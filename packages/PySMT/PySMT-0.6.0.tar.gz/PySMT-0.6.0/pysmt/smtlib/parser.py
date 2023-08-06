#
# This file is part of pySMT.
#
#   Copyright 2014 Andrea Micheli and Marco Gario
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import functools
import itertools

from warnings import warn
from six import iteritems, PY2
from six.moves import xrange

import pysmt.smtlib.commands as smtcmd
from pysmt.environment import get_env
from pysmt.typing import BOOL, REAL, INT, FunctionType, BVType, ArrayType
from pysmt.logics import get_logic_by_name, UndefinedLogicError
from pysmt.exceptions import UnknownSmtLibCommandError
from pysmt.smtlib.script import SmtLibCommand, SmtLibScript
from pysmt.smtlib.annotations import Annotations
from pysmt.utils import interactive_char_iterator
from pysmt.constants import Fraction


def open_(fname):
    """Transparently handle .bz2 files."""
    if fname.endswith(".bz2"):
        import bz2
        if PY2:
            return bz2.BZ2File(fname, "r")
        else:
            return bz2.open(fname, "rt")
    return open(fname)

def get_formula(script_stream, environment=None):
    """
    Returns the formula asserted at the end of the given script

    script_stream is a file descriptor.
    """
    mgr = None
    if environment is not None:
        mgr = environment.formula_manager

    parser = SmtLibParser(environment)
    script = parser.get_script(script_stream)
    return script.get_last_formula(mgr)


def get_formula_strict(script_stream, environment=None):
    """Returns the formula defined in the SMTScript.

    This function assumes that only one formula is defined in the
    SMTScript. It will raise an exception if commands such as pop and
    push are present in the script, or if check-sat is called more
    than once.
    """
    mgr = None
    if environment is not None:
        mgr = environment.formula_manager

    parser = SmtLibParser(environment)
    script = parser.get_script(script_stream)
    return script.get_strict_formula(mgr)


def get_formula_fname(script_fname, environment=None, strict=True):
    """Returns the formula asserted at the end of the given script."""
    with open_(script_fname) as script:
        if strict:
            return get_formula_strict(script, environment)
        else:
            return get_formula(script, environment)


class SmtLibExecutionCache(object):
    """Execution environment for SMT2 script execution"""
    def __init__(self):
        self.keys = {}
        self.definitions = {}
        self.annotations = Annotations()

    def bind(self, name, value):
        """Binds a symbol in this environment"""
        lst = self.keys.setdefault(name, [])
        lst.append(value)

    def unbind(self, name):
        """Unbinds the last binding of this symbol"""
        self.keys[name].pop()

    def define(self, name, parameters, expression):
        self.definitions[name] = (parameters, expression)

    def _define_adapter(self, formal_parameters, expression):
        def res(*actual_parameters):
            assert len(formal_parameters) == len(actual_parameters)
            submap = dict(zip(formal_parameters, actual_parameters))
            return expression.substitute(submap)
        return res

    def get(self, name):
        """Returns the last binding for 'name'"""
        if name in self.definitions:
            (parameters, expression) = self.definitions[name]
            if len(parameters) == 0:
                return expression
            return self._define_adapter(parameters, expression)
        elif name in self.keys:
            lst = self.keys[name]
            if len(lst) > 0:
                return lst[-1]
            else:
                return None
        else:
            return None

    def update(self, value_map):
        """Binds all the symbols in 'value_map'"""
        for k, val in iteritems(value_map):
            self.bind(k, val)

    def unbind_all(self, values):
        """UnBinds all the symbols in 'values'"""
        for k in values:
            self.unbind(k)



def tokenizer(handle, interactive=False):
    """Takes a file-like object and produces a stream of tokens following
    the LISP rules.

    If interative is True, the file reading proceeds char-by-char with
    no buffering. This is useful for interactive use for example with
    a SMT-Lib2-compliant solver
    """
    spaces = set([" ", "\n", "\t"])
    separators = set(["(", ")", "|", "\""])
    specials = spaces | separators | set([";", ""])

    if not interactive:
        reader = itertools.chain.from_iterable(handle) # reads char-by-char
    else:
        reader = interactive_char_iterator(handle)
    c = next(reader)

    eof = False
    while not eof:
        if c in specials:
            # consume the spaces
            if c in spaces:
                c = next(reader)

            elif c in separators:
                if c == "|":
                    s = []
                    c = next(reader)
                    while c and c != "|":
                        if c == "\\": # This is a single '\'
                            c = next(reader)
                            if c != "|" and c != "\\":
                                # Only \| and \\ are supported escapings
                                raise SyntaxError("Unknown escaping in " \
                                                  "quoted symbol: '\\%s'" % c)
                        s.append(c)
                        c = next(reader)
                    if not c:
                        raise SyntaxError("Expected '|'")
                    yield "".join(s)
                    c = next(reader)

                elif c == "\"":
                    # String literals
                    s = []
                    c = next(reader)
                    while c:
                        if c == "\"":
                            c = next(reader)
                            if c == "\"":
                                s.append(c)
                                c = next(reader)
                            else:
                                break
                        else:
                            s.append(c)
                            c = next(reader)
                    if not c:
                        raise SyntaxError("Expected '|'")
                    yield '"%s"' % ("".join(s)) # string literals maintain their quoting

                else:
                    yield c
                    c = next(reader)

            elif c == ";":
                while c and c != "\n":
                    c = next(reader)
                c = next(reader)

            else:
                # EOF
                eof = True
                assert len(c) == 0
        else:
            tk = []
            while c not in specials:
                tk.append(c)
                c = next(reader)
            yield "".join(tk)



class SmtLibParser(object):
    """Parse an SmtLib file and builds an SmtLibScript object.

    The main function is get_script (and its wrapper
    get_script_fname).  This function relies on the tokenizer function
    (to split the inputs in token) that is consumed by the get_command
    function that returns a SmtLibCommand for each command in the
    original file.

    If the interactive flag is True, the file reading proceeds
    char-by-char with no buffering. This is useful for interactive use
    for example with a SMT-Lib2-compliant solver
    """

    def __init__(self, environment=None, interactive=False):
        self.env = get_env() if environment is None else environment
        self.interactive = interactive

        # Placeholders for fields filled by self._reset
        self.cache = None
        self.logic = None
        self._reset()

        # Tokens representing interpreted functions appearing in expressions
        # Each token is handled by a dedicated function that takes the
        # recursion stack, the token stream and the parsed token
        # Common tokens are handled in the _reset function
        mgr = self.env.formula_manager
        self.interpreted = {"let" : self._enter_let,
                            "!" : self._enter_annotation,
                            "exists" : self._enter_quantifier,
                            "forall" : self._enter_quantifier,
                            '+':self._operator_adapter(mgr.Plus),
                            '-':self._operator_adapter(self._minus_or_uminus),
                            '*':self._operator_adapter(mgr.Times),
                            '/':self._operator_adapter(self._division),
                            'pow':self._operator_adapter(mgr.Pow),
                            '>':self._operator_adapter(mgr.GT),
                            '<':self._operator_adapter(mgr.LT),
                            '>=':self._operator_adapter(mgr.GE),
                            '<=':self._operator_adapter(mgr.LE),
                            '=':self._operator_adapter(self._equals_or_iff),
                            'not':self._operator_adapter(mgr.Not),
                            'and':self._operator_adapter(mgr.And),
                            'or':self._operator_adapter(mgr.Or),
                            'xor':self._operator_adapter(mgr.Xor),
                            '=>':self._operator_adapter(mgr.Implies),
                            '<->':self._operator_adapter(mgr.Iff),
                            'ite':self._operator_adapter(mgr.Ite),
                            'to_real':self._operator_adapter(mgr.ToReal),
                            'concat':self._operator_adapter(mgr.BVConcat),
                            'bvnot':self._operator_adapter(mgr.BVNot),
                            'bvand':self._operator_adapter(mgr.BVAnd),
                            'bvor':self._operator_adapter(mgr.BVOr),
                            'bvneg':self._operator_adapter(mgr.BVNeg),
                            'bvadd':self._operator_adapter(mgr.BVAdd),
                            'bvmul':self._operator_adapter(mgr.BVMul),
                            'bvudiv':self._operator_adapter(mgr.BVUDiv),
                            'bvurem':self._operator_adapter(mgr.BVURem),
                            'bvshl':self._operator_adapter(mgr.BVLShl),
                            'bvlshr':self._operator_adapter(mgr.BVLShr),
                            'bvsub':self._operator_adapter(mgr.BVSub),
                            'bvult':self._operator_adapter(mgr.BVULT),
                            'bvxor':self._operator_adapter(mgr.BVXor),
                            '_':self._smtlib_underscore,
                            # Extended Functions
                            'bvnand':self._operator_adapter(mgr.BVNand),
                            'bvnor':self._operator_adapter(mgr.BVNor),
                            'bvxnor':self._operator_adapter(mgr.BVXnor),
                            'bvcomp':self._operator_adapter(mgr.BVComp),
                            'bvsdiv':self._operator_adapter(mgr.BVSDiv),
                            'bvsrem':self._operator_adapter(mgr.BVSRem),
                            'bvsmod':self._operator_adapter(mgr.BVSMod),
                            'bvashr':self._operator_adapter(mgr.BVAShr),
                            'bvule':self._operator_adapter(mgr.BVULE),
                            'bvugt':self._operator_adapter(mgr.BVUGT),
                            'bvuge':self._operator_adapter(mgr.BVUGE),
                            'bvslt':self._operator_adapter(mgr.BVSLT),
                            'bvsle':self._operator_adapter(mgr.BVSLE),
                            'bvsgt':self._operator_adapter(mgr.BVSGT),
                            'bvsge':self._operator_adapter(mgr.BVSGE),
                            # arrays
                            'select':self._operator_adapter(mgr.Select),
                            'store':self._operator_adapter(mgr.Store),
                            'as':self._enter_smtlib_as,
                            }

        # Command tokens
        self.commands = {smtcmd.ASSERT : self._cmd_assert,
                         smtcmd.CHECK_SAT : self._cmd_check_sat,
                         smtcmd.CHECK_SAT_ASSUMING : self._cmd_check_sat_assuming,
                         smtcmd.DECLARE_CONST : self._cmd_declare_const,
                         smtcmd.DECLARE_FUN : self._cmd_declare_fun,
                         smtcmd.DECLARE_SORT: self._cmd_declare_sort,
                         smtcmd.DEFINE_FUN : self._cmd_define_fun,
                         smtcmd.DEFINE_FUNS_REC : self._cmd_define_funs_rec,
                         smtcmd.DEFINE_FUN_REC : self._cmd_define_fun_rec,
                         smtcmd.DEFINE_SORT: self._cmd_define_sort,
                         smtcmd.ECHO : self._cmd_echo,
                         smtcmd.EXIT : self._cmd_exit,
                         smtcmd.GET_ASSERTIONS: self._cmd_get_assertions,
                         smtcmd.GET_ASSIGNMENT : self._cmd_get_assignment,
                         smtcmd.GET_INFO: self._cmd_get_info,
                         smtcmd.GET_MODEL: self._cmd_get_model,
                         smtcmd.GET_OPTION: self._cmd_get_option,
                         smtcmd.GET_PROOF: self._cmd_get_proof,
                         smtcmd.GET_UNSAT_ASSUMPTIONS : self._cmd_get_unsat_assumptions,
                         smtcmd.GET_UNSAT_CORE: self._cmd_get_unsat_core,
                         smtcmd.GET_VALUE : self._cmd_get_value,
                         smtcmd.POP : self._cmd_pop,
                         smtcmd.PUSH : self._cmd_push,
                         smtcmd.RESET : self._cmd_reset,
                         smtcmd.RESET_ASSERTIONS : self._cmd_reset_assertions,
                         smtcmd.SET_LOGIC : self._cmd_set_logic,
                         smtcmd.SET_OPTION : self._cmd_set_option,
                         smtcmd.SET_INFO : self._cmd_set_info,
                     }

    def _reset(self):
        """Resets the parser to the initial state"""
        self.cache = SmtLibExecutionCache()
        self.logic = None
        mgr = self.env.formula_manager
        self.cache.update({'false':mgr.FALSE(), 'true':mgr.TRUE()})


    def _minus_or_uminus(self, *args):
        """Utility function that handles both unary and binary minus"""
        mgr = self.env.formula_manager
        if len(args) == 1:
            lty = self.env.stc.get_type(args[0])
            mult = None
            if lty == INT:
                if args[0].is_int_constant():
                    return mgr.Int(-1 * args[0].constant_value())
                mult = mgr.Int(-1)
            else:
                if args[0].is_real_constant():
                    return mgr.Real(-1 * args[0].constant_value())
                mult = mgr.Real(-1)
            return mgr.Times(mult, args[0])
        else:
            assert len(args) == 2
            return mgr.Minus(args[0], args[1])


    def _enter_smtlib_as(self, stack, tokens, key):
        """Utility function that handles 'as' that is a special function in SMTLIB"""
        #pylint: disable=unused-argument
        const = self.parse_atom(tokens, "expression")
        if const != "const":
            raise SyntaxError("expected 'const' in expression after 'as'")
        tyname = self.parse_type(tokens, "expression")
        ty = self._get_basic_type(tyname)

        def res(expr):
            return self.env.formula_manager.Array(ty.index_type, expr)
        def handler():
            return res
        stack[-1].append(handler)


    def _smtlib_underscore(self, stack, tokens, key):
        #pylint: disable=unused-argument
        """Utility function that handles _ special function in SMTLIB"""
        mgr = self.env.formula_manager

        op = self.parse_atom(tokens, "expression")

        fun = None
        if op == "extract":
            send = self.parse_atom(tokens, "expression")
            sstart = self.parse_atom(tokens, "expression")
            try:
                start = int(sstart)
                end = int(send)
            except ValueError:
                raise SyntaxError("Expected number in '_ extract' expression")
            fun = lambda x : mgr.BVExtract(x, start, end)

        elif op == "zero_extend":
            swidth = self.parse_atom(tokens, "expression")
            try:
                width = int(swidth)
            except ValueError:
                raise SyntaxError("Expected number in '_ zero_extend' expression")
            fun = lambda x: mgr.BVZExt(x, width)

        elif op == "repeat":
            scount = self.parse_atom(tokens, "expression")
            try:
                count = int(scount)
            except ValueError:
                raise SyntaxError("Expected number in '_ repeat' expression")
            fun = lambda x: mgr.BVRepeat(x, count)

        elif op == "rotate_left":
            sstep = self.parse_atom(tokens, "expression")
            try:
                step = int(sstep)
            except ValueError:
                raise SyntaxError("Expected number in '_ rotate_left' expression")
            fun = lambda x: mgr.BVRol(x, step)

        elif op == "rotate_right":
            sstep = self.parse_atom(tokens, "expression")
            try:
                step = int(sstep)
            except ValueError:
                raise SyntaxError("Expected number in '_ rotate_left' expression")
            fun = lambda x: mgr.BVRor(x, step)

        elif op == "sign_extend":
            swidth = self.parse_atom(tokens, "expression")
            try:
                width = int(swidth)
            except ValueError:
                raise SyntaxError("Expected number in '(_ sign_extend) expression'")
            fun = lambda x: mgr.BVSExt(x, width)

        elif op.startswith("bv"):
            try:
                v = int(op[2:])
                width = int(self.parse_atom(tokens, "expression"))
            except ValueError:
                raise SyntaxError("Expected number in '_ bv' expression: '%s'" % op)
            fun = mgr.BV(v, width)

        else:
            raise SyntaxError("Unexpected '_' expression '%s'" % op)

        # Consume the closed parenthesis of the (_ ...) term and add the
        # resulting function to the correct level in the stack
        self.consume_closing(tokens, "expression")
        stack.pop()
        stack[-1].append(fun)



    def _equals_or_iff(self, left, right):
        """Utility function that treats = between booleans as <->"""
        mgr = self.env.formula_manager
        lty = self.env.stc.get_type(left)
        if lty == BOOL:
            return mgr.Iff(left, right)
        else:
            return mgr.Equals(left, right)

    def _division(self, left, right):
        """Utility function that builds a division"""
        mgr = self.env.formula_manager
        if left.is_constant() and right.is_constant():
            return mgr.Real(Fraction(left.constant_value()) / \
                            Fraction(right.constant_value()))
        return mgr.Div(left, right)

    def _get_basic_type(self, type_name, params=None):
        """
        Returns the pysmt type representation for the given type name.
        If params is specified, the type is interpreted as a function type.
        """
        if params is None or len(params) == 0:
            if isinstance(type_name, tuple):
                assert len(type_name) == 3
                assert type_name[0] == "Array"
                return ArrayType(self._get_basic_type(type_name[1]),
                                 self._get_basic_type(type_name[2]))

            if type_name == "Bool":
                return BOOL
            elif type_name == "Int":
                return INT
            elif type_name == "Real":
                return REAL
            elif type_name.startswith("BV"):
                size = int(type_name[2:])
                return BVType(size)
            else:
                res = self.cache.get(type_name)
                if res is not None:
                    res = self._get_basic_type(res)
                return res
        else:
            rt = self._get_basic_type(type_name)
            pt = [self._get_basic_type(par) for par in params]
            return FunctionType(rt, pt)

    def _get_var(self, name, type_name, params=None):
        """Returns the PySMT variable corresponding to a declaration"""
        typename = self._get_basic_type(type_name, params)
        return self.env.formula_manager.Symbol(name=name,
                                                        typename=typename)
    def atom(self, token, mgr):
        """
        Given a token and a FormulaManager, returns the pysmt representation of
        the token
        """
        res = self.cache.get(token)
        if res is None:
            if token.startswith("#"):
                # it is a BitVector
                value = None
                width = None
                if token[1] == "b":
                    # binary
                    width = len(token) - 2
                    value = int("0" + token[1:], 2)
                else:
                    if token[1] != "x":
                        raise SyntaxError("Invalid bit-vector constant '%s'" % token)
                    width = (len(token) - 2) * 16
                    value = int("0" + token[1:], 16)
                res = mgr.BV(value, width)
            else:
                # it could be a number or a string
                try:
                    frac = Fraction(token)
                    if frac.denominator == 1:
                        # We found an integer, depending on the logic this can be
                        # an Int or a Real
                        if self.logic is None or \
                           self.logic.theory.integer_arithmetic:
                            if "." in token:
                                res = mgr.Real(frac)
                            else:
                                res = mgr.Int(frac.numerator)
                        else:
                            res = mgr.Real(frac)
                    else:
                        res = mgr.Real(frac)

                except ValueError:
                    # a string constant
                    res = token
            self.cache.bind(token, res)
        return res

    def _exit_let(self, varlist, bdy):
        """ Cleans the execution environment when we exit the scope of a 'let' """
        for k in varlist:
            self.cache.unbind(k)
        return bdy

    def _exit_quantifier(self, fun, vrs, body):
        """
        Cleans the execution environment when we exit the scope of a quantifier
        """
        for var in vrs:
            self.cache.unbind(var.symbol_name())
        return fun(vrs, body)

    def _exit_annotation(self, pyterm, *attrs):
        """
        This method is invoked when we finish parsing an annotated expression
        """

        # Iterate on elements.
        i = 0
        while i < len(attrs):
            if i+1 < len(attrs) and str(attrs[i+1])[0] != ":" :
                key, value = str(attrs[i]), str(attrs[i+1])
                if key[0] != ":":
                    raise SyntaxError("Annotations keys should start with colon")
                self.cache.annotations.add(pyterm, key[1:], value)
                i += 2
            else:
                key = str(attrs[i])
                if key[0] != ":":
                    raise SyntaxError("Annotations keys should start with colon")
                self.cache.annotations.add(pyterm, key[1:])
                i += 1

        return pyterm

    def _enter_let(self, stack, tokens, key):
        """Handles a let expression by recurring on the expression and
        updating the cache
        """
        #pylint: disable=unused-argument
        self.consume_opening(tokens, "expression")
        newvals = {}
        current = "("
        self.consume_opening(tokens, "expression")
        while current != ")":
            if current != "(":
                raise SyntaxError("Expected '(' in let binding")
            vname = self.parse_atom(tokens, "expression")
            expr = self.get_expression(tokens)
            newvals[vname] = expr
            self.cache.bind(vname, expr)
            self.consume_closing(tokens, "expression")
            current = next(tokens)

        stack[-1].append(self._exit_let)
        stack[-1].append(newvals.keys())

    def _operator_adapter(self, operator):
        """Handles generic operator"""
        def res(stack, tokens, key):
            #pylint: disable=unused-argument
            stack[-1].append(operator)
        return res

    def _enter_quantifier(self, stack, tokens, key):
        """Handles quantifiers by defining the bound variable in the cache
        before parsing the matrix
        """
        mgr = self.env.formula_manager
        vrs = []
        self.consume_opening(tokens, "expression")
        current = "("
        self.consume_opening(tokens, "expression")
        while current != ")":
            if current != "(":
                raise SyntaxError("Expected '(' in let binding")
            vname = self.parse_atom(tokens, "expression")
            typename = self.parse_type(tokens, "expression")

            var = self._get_var(vname, typename)
            self.cache.bind(vname, var)
            vrs.append(var)

            self.consume_closing(tokens, "expression")
            current = next(tokens)

        quant = None
        if key == 'forall':
            quant = mgr.ForAll
        else:
            quant = mgr.Exists

        stack[-1].append(self._exit_quantifier)
        stack[-1].append(quant)
        stack[-1].append(vrs)


    def _enter_annotation(self, stack, tokens, key):
        """Deals with annotations"""
        #pylint: disable=unused-argument
        stack[-1].append(self._exit_annotation)


    def get_expression(self, tokens):
        """
        Returns the pysmt representation of the given parsed expression
        """
        mgr = self.env.formula_manager
        stack = []

        while True:
            tk = next(tokens)

            if tk == "(":
                while tk == "(":
                    stack.append([])
                    tk = next(tokens)

                if tk in self.interpreted:
                    fun = self.interpreted[tk]
                    fun(stack, tokens, tk)
                else:
                    stack[-1].append(self.atom(tk, mgr))

            elif tk == ")":
                try:
                    lst = stack.pop()
                    fun = lst.pop(0)
                except IndexError:
                    raise SyntaxError("Unexpected ')'")

                try:
                    res = fun(*lst)
                except TypeError as err:
                    if not callable(fun):
                        raise NotImplementedError("Unknown function '%s'" % fun)
                    raise err

                if len(stack) > 0:
                    stack[-1].append(res)
                else:
                    return res

            else:
                try:
                    stack[-1].append(self.atom(tk, mgr))
                except IndexError:
                    return self.atom(tk, mgr)



    def get_script(self, script):
        """
        Takes a file object and returns a SmtLibScript object representing the file
        """
        self._reset() # prepare the parser
        res = SmtLibScript()
        for cmd in self.get_command_generator(script):
            res.add_command(cmd)
        res.annotations = self.cache.annotations
        return res

    def get_command_generator(self, script):
        """Returns a python generator of SmtLibCommand's given a file object
        to read from

        This function can be used interactively, and blocks until a
        whole command is read from the script.

        """
        tokens = tokenizer(script, interactive=self.interactive)
        for cmd in self.get_command(tokens):
            yield cmd

    def get_script_fname(self, script_fname):
        """Given a filename and a Solver, executes the solver on the file."""
        with open_(script_fname) as script:
            return self.get_script(script)

    def parse_atoms(self, tokens, command, min_size, max_size=None):
        """
        Parses a sequence of N atoms (min_size <= N <= max_size) consuming
        the tokens
        """
        if max_size is None:
            max_size = min_size

        res = []
        current = None
        for _ in xrange(min_size):
            current = next(tokens)
            if current == ")":
                raise SyntaxError("Expected at least %d arguments in %s command." %\
                                  (min_size, command))
            if current == "(":
                raise SyntaxError("Unexpected token '(' in %s command." % command)
            res.append(current)

        for _ in xrange(min_size, max_size + 1):
            current = next(tokens)
            if current == ")":
                return res
            if current == "(":
                raise SyntaxError("Unexpected token '(' in %s command." % command)
            res.append(current)
        raise SyntaxError("Unexpected token '%s' in %s command. Expected at " \
                          "most %d arguments." % (current, command, max_size))


    def parse_type(self, tokens, command, additional_token=None):
        """Parses a single type name from the tokens"""
        if additional_token is not None:
            var = additional_token
        else:
            var = next(tokens)
        if var == "(":
            op = next(tokens)

            if op == "Array":
                idxtype = self.parse_type(tokens, command)
                elemtype = self.parse_type(tokens, command)
                self.consume_closing(tokens, command)
                return ("Array", idxtype, elemtype)

            if op != "_":
                raise SyntaxError("Unexpected token '%s' in %s command." % \
                                  (op, command))
            ts = next(tokens)
            if ts != "BitVec":
                raise SyntaxError("Unexpected token '%s' in %s command." % \
                                  (ts, command))

            size = 0
            dim = next(tokens)
            try:
                size = int(dim)
            except ValueError:
                raise SyntaxError("Unexpected token '%s' in %s command." % \
                                  (dim, command))

            self.consume_closing(tokens, command)
            return "BV%d" % size

        elif var == ")":
            raise SyntaxError("Unexpected token '%s' in %s command." % \
                              (var, command))
        return var


    def parse_atom(self, tokens, command):
        """Parses a single name from the tokens"""
        var = next(tokens)
        if var == "(" or var == ")":
            raise SyntaxError("Unexpected token '%s' in %s command." % \
                              (var, command))
        return var

    def parse_params(self, tokens, command):
        """Parses a list of types from the tokens"""
        self.consume_opening(tokens, command)
        current = next(tokens)
        res = []
        while current != ")":
            res.append(self.parse_type(tokens, command,additional_token=current))
            current = next(tokens)
        return res

    def parse_named_params(self, tokens, command):
        """Parses a list of names and type from the tokens"""
        self.consume_opening(tokens, command)
        current = next(tokens)
        res = []
        while current != ")":
            vname = self.parse_atom(tokens, command)
            typename = self.parse_type(tokens, command)
            res.append((vname, typename))
            self.consume_closing(tokens, command)
            current = next(tokens)
        return res

    def parse_expr_list(self, tokens, command):
        """Parses a list of expressions form the tokens"""
        self.consume_opening(tokens, command)
        res = []
        while True:
            try:
                current = self.get_expression(tokens)
                res.append(current)
            except SyntaxError:
                return res

    def consume_opening(self, tokens, command):
        """ Consumes a single '(' """
        p = next(tokens)
        if p != "(":
            raise SyntaxError("Unexpected token '%s' in %s command. " \
                              "Expected '('" % (p, command))

    def consume_closing(self, tokens, command):
        """ Consumes a single ')' """
        p = next(tokens)
        if p != ")":
            raise SyntaxError("Unexpected token '%s' in %s command. " \
                              "Expected ')'" % (p, command))

    def _function_call_helper(self, v, *args):
        """ Helper function for dealing with function calls """
        return self.env.formula_manager.Function(v, args)

    def get_assignment_list(self, script):
        """
        Parse an assignment list produced by get-model and get-value
        commands in SmtLib
        """
        symbols = self.env.formula_manager.symbols
        self.cache.update(symbols)
        tokens = tokenizer(script, interactive=self.interactive)
        res = []
        self.consume_opening(tokens, "<main>")
        current = next(tokens)
        while current != ")":
            if current != "(":
                raise SyntaxError("'(' expected")
            vname = self.get_expression(tokens)
            expr = self.get_expression(tokens)
            self.consume_closing(tokens, current)
            res.append((vname, expr))
            current = next(tokens)
        self.cache.unbind_all(symbols)
        return res

    def get_command(self, tokens):
        """Builds an SmtLibCommand instance out of a parsed term."""
        while True:
            self.consume_opening(tokens, "<main>")
            current = next(tokens)
            if current in self.commands:
                fun = self.commands[current]
                yield fun(current, tokens)
            else:
                raise UnknownSmtLibCommandError(current)

    def _cmd_not_implemented(self, current, tokens):
        raise NotImplementedError("'%s' has not been implemented yet" % current)

    def _cmd_set_info(self, current, tokens):
        """(set-info <attribute>)"""
        elements = self.parse_atoms(tokens, current, 2)
        return SmtLibCommand(current, elements)

    def _cmd_set_option(self, current, tokens):
        """(set-option <option>)"""
        elements = self.parse_atoms(tokens, current, 2)
        return SmtLibCommand(current, elements)

    def _cmd_assert(self, current, tokens):
        """(assert <term>)"""
        expr = self.get_expression(tokens)
        self.consume_closing(tokens, current)
        return SmtLibCommand(current, [expr])

    def _cmd_check_sat(self, current, tokens):
        """(check-sat)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_push(self, current, tokens):
        """(push <numeral>)"""
        elements = self.parse_atoms(tokens, current, 0, 1)
        levels = 1
        if len(elements) > 0:
            levels = int(elements[0])
        return SmtLibCommand(current, [levels])

    def _cmd_pop(self, current, tokens):
        """(pop <numeral>)"""
        elements = self.parse_atoms(tokens, current, 0, 1)
        levels = 1
        if len(elements) > 0:
            levels = int(elements[0])
        return SmtLibCommand(current, [levels])

    def _cmd_exit(self, current, tokens):
        """(exit)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_set_logic(self, current, tokens):
        """(set-logic <symbol>)"""
        elements = self.parse_atoms(tokens, current, 1)
        name = elements[0]
        try:
            self.logic = get_logic_by_name(name)
            return SmtLibCommand(current, [self.logic])
        except UndefinedLogicError:
            warn("Unknown logic '" + name + \
                 "'. Ignoring set-logic command.")
            return SmtLibCommand(current, [None])

    def _cmd_declare_const(self, current, tokens):
        """(declare-const <symbol> <sort>)"""
        elements = self.parse_atoms(tokens, current, 2)
        (var, typename) = elements
        v = self._get_var(var, typename)
        self.cache.bind(var, v)
        return SmtLibCommand(current, [v])

    def _cmd_get_value(self, current, tokens):
        """(get-value (<term>+)"""
        params = self.parse_expr_list(tokens, current)
        self.consume_closing(tokens, current)
        return SmtLibCommand(current, params)

    def _cmd_declare_fun(self, current, tokens):
        """(declare-fun <symbol> (<sort>*) <sort>)"""
        var = self.parse_atom(tokens, current)
        params = self.parse_params(tokens, current)
        typename = self.parse_type(tokens, current)
        self.consume_closing(tokens, current)

        v = self._get_var(var, typename, params)
        if v.symbol_type().is_function_type():
            self.cache.bind(var, \
                    functools.partial(self._function_call_helper, v))
        else:
            self.cache.bind(var, v)
        return SmtLibCommand(current, [v])

    def _cmd_define_fun(self, current, tokens):
        """(define-fun <fun_def>)"""
        formal = []
        var = self.parse_atom(tokens, current)
        namedparams = self.parse_named_params(tokens, current)
        rtype = self.parse_type(tokens, current)

        for (x,t) in namedparams:
            v = self._get_var(x, t)
            self.cache.bind(x, v)
            formal.append(v)
        # Parse expression using also parameters
        ebody = self.get_expression(tokens)
        # Discard parameters
        for x in formal:
            self.cache.unbind(x.symbol_name())
        # Finish Parsing
        self.consume_closing(tokens, current)
        self.cache.define(var, formal, ebody)
        return SmtLibCommand(current, [var, formal, rtype, ebody])

    def _cmd_declare_sort(self, current, tokens):
        """(declare-sort <symbol> <numeral>)"""
        return self._cmd_not_implemented(current, tokens)

    def _cmd_define_sort(self, current, tokens):
        """(define-sort <fun_def>)"""
        name = self.parse_atom(tokens, current)
        self.consume_opening(tokens, current)
        cur = next(tokens)
        if cur != ')':
            return self._cmd_not_implemented(current, tokens)
        rtype = self.parse_type(tokens, current)
        self.consume_closing(tokens, current)
        self.cache.define(name, [], rtype)
        return SmtLibCommand(current, [name, [], rtype])

    def _cmd_get_assertions(self, current, tokens):
        """(get_assertions)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_get_info(self, current, tokens):
        """(get-info <info_flag>)"""
        keyword = self.parse_atoms(tokens, current, 1)
        return SmtLibCommand(current, keyword)

    def _cmd_get_model(self, current, tokens):
        """(get-model)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_get_option(self, current, tokens):
        """(get-option <keyword>)"""
        keyword = self.parse_atoms(tokens, current, 1)
        return SmtLibCommand(current, keyword)

    def _cmd_get_proof(self, current, tokens):
        """(get-proof)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_get_unsat_core(self, current, tokens):
        """(get-unsat-core)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_check_sat_assuming(self, current, tokens):
        """(check-sat-assuming (<prop_literal>*) ) """
        params = self.parse_expr_list(tokens, current)
        self.consume_closing(tokens, current)
        return SmtLibCommand(current, params)

    def _cmd_define_fun_rec(self, current, tokens):
        """(define-fun-rec <fun_def>)"""
        return self._cmd_not_implemented(current, tokens)

    def _cmd_define_funs_rec(self, current, tokens):
        """(define-funs-rec (<fun_dec>^{n+1}) (<term>^{n+1>))"""
        return self._cmd_not_implemented(current, tokens)

    def _cmd_echo(self, current, tokens):
        """(echo <string>)"""
        elements = self.parse_atoms(tokens, current, 1)
        return SmtLibCommand(current, elements)

    def _cmd_get_assignment(self, current, tokens):
        """(get-assignment)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_get_unsat_assumptions(self, current, tokens):
        """(get-unsat-assumptions)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_reset(self, current, tokens):
        """(reset)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])

    def _cmd_reset_assertions(self, current, tokens):
        """(reset-assertions)"""
        self.parse_atoms(tokens, current, 0)
        return SmtLibCommand(current, [])


class SmtLib20Parser(SmtLibParser):
    """Parser for SMT-LIB 2.0."""

    def __init__(self, environment=None, interactive=False):
        SmtLibParser.__init__(self, environment, interactive)

        # Remove commands that were introduced in SMT-LIB 2.5
        del self.commands["check-sat-assuming"]
        del self.commands["declare-const"]
        del self.commands["define-fun-rec"]
        del self.commands["define-funs-rec"]
        del self.commands["echo"]
        del self.commands["get-assignment"]
        del self.commands["get-unsat-assumptions"]
        del self.commands["reset"]
        del self.commands["reset-assertions"]


class SmtLibZ3Parser(SmtLibParser):
    """
    Parses extended Z3 SmtLib Syntax
    """
    def __init__(self, environment=None, interactive=False):
        SmtLibParser.__init__(self, environment, interactive)

        # Z3 prints Pow as "^"
        self.interpreted["^"] = self.interpreted["pow"]
        self.interpreted["ext_rotate_left"] = self._operator_adapter(self._ext_rotate_left)
        self.interpreted["ext_rotate_right"] = self._operator_adapter(self._ext_rotate_right)

    def _ext_rotate_left(self, x, y):
        return self.env.formula_manager.BVRol(x, y.simplify().constant_value())

    def _ext_rotate_right(self, x, y):
        return self.env.formula_manager.BVRor(x, y.simplify().constant_value())



if __name__ == "__main__":
    import sys

    def main():
        """Simple testing script"""
        args = sys.argv
        out = None
        if len(args) == 3:
            out = args[2]
        elif len(args) != 2:
            print("Usage %s <file.smt2> [out.smt2]" % args[0])
            exit(1)

        fname = args[1]

        parser = SmtLibParser()
        res = parser.get_script_fname(fname)
        assert res is not None
        print("Done")
        if out is not None:
            res.to_file(out, daggify=True)
    main()
