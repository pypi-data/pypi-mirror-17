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

from pysmt.test import TestCase, main
from pysmt.test import skipIfNoSolverForLogic, skipIfSolverNotAvailable
from pysmt.logics import QF_AUFLIA, QF_AUFBV
from pysmt.typing import ARRAY_INT_INT, ArrayType, INT, REAL, BV8
from pysmt.shortcuts import (Solver,
                             Symbol, Not, Equals, Int, BV, Real, FreshSymbol,
                             Select, Store, Array)
from pysmt.exceptions import ConvertExpressionError


class TestArray(TestCase):

    def test_array_type(self):
        aii_type = ARRAY_INT_INT
        aii_type2 = ArrayType(INT, INT)
        self.assertEqual(aii_type, aii_type2)

    def test_nested_array_type(self):
        base = ARRAY_INT_INT
        nested = ArrayType(base, base)
        self.assertIsNotNone(nested)

        idx_type = nested.index_type
        elem_type = nested.elem_type
        self.assertEqual(idx_type, base)
        self.assertEqual(elem_type, base)

        # Equality tests
        nested2 = ArrayType(ArrayType(INT, INT),
                            ArrayType(INT, INT))
        self.assertEqual(nested, nested2)

        fake_nested = ArrayType(ArrayType(INT, INT),
                                ArrayType(INT, REAL))
        self.assertNotEqual(nested, fake_nested)


    @skipIfNoSolverForLogic(QF_AUFLIA)
    def test_array(self):
        a = Symbol("a", ARRAY_INT_INT)
        formula = Equals(Select(Store(a, Int(10), Int(100)), Int(10)),
                         Int(100))
        self.assertSat(formula, logic=QF_AUFLIA)

    @skipIfNoSolverForLogic(QF_AUFBV)
    def test_bv_array(self):
        a = Symbol("a", ArrayType(BV8, BV8))
        formula = Equals(Select(Store(a, BV(10, 8), BV(100, 8)), BV(10,8)),
                         BV(100,8))
        self.assertSat(formula, logic=QF_AUFBV)

    @skipIfSolverNotAvailable("btor")
    def test_btor_does_not_support_int_arrays(self):
        a = Symbol("a", ARRAY_INT_INT)
        formula = Equals(Select(Store(a, Int(10), Int(100)), Int(10)),
                         Int(100))
        btor = Solver(name="btor")
        with self.assertRaises(ConvertExpressionError):
            btor.add_assertion(formula)

    @skipIfSolverNotAvailable("btor")
    def test_btor_does_not_support_const_arryas(self):
        with self.assertRaises(ConvertExpressionError):
            btor = Solver(name="btor")
            btor.add_assertion(Equals(Array(BV8, BV(0, 8)),
                                      FreshSymbol(ArrayType(BV8, BV8))))

    def test_complex_types(self):
        with self.assertRaises(TypeError):
            # Not(Store(Array<Real,BV8>(8d_0), 1.0, 8d_5) =
            #     Store(Array<Int,BV8>(8d_0), 1, 8d_5))
            Not(Equals(Store(Array(REAL, BV(0, 8)), Real(1), BV(5, 8)),
                       Store(Array(INT,  BV(0, 8)), Int(1), BV(5, 8))))

        nested_a = Symbol("a_arb_aii", ArrayType(ArrayType(REAL, BV8),
                                                 ARRAY_INT_INT))
        with self.assertRaises(TypeError):
        # This is wrong, because the first elemnt of Array must be a Type
            Equals(nested_a, Array(Array(REAL, BV(0,8)),
                                   Array(INT, Int(7))))

    def test_is_array_op(self):
        a = Symbol("a", ARRAY_INT_INT)
        store_ = Store(a, Int(10), Int(100))
        select_ = Select(store_, Int(100))
        self.assertTrue(store_.is_array_op())
        self.assertTrue(select_.is_array_op())


if __name__ == "__main__":
    main()
