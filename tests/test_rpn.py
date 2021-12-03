import unittest
import numpy
from rpncalc.rpncalc import parse_expression, compute_rpn
import rpncalc.storedvalues
import rpncalc.util


class TestRPNCalc(unittest.TestCase):

    def run_from_expr(self, expr, clear_stored=True, clear_stack=True):
        print(f"\n\"{expr}\"")
        ans = compute_rpn(parse_expression(expr))
        # Clear the named storage variables to ensure
        # that unittests are independent of order
        if clear_stored:
            rpncalc.storedvalues.clear_storage()
        if clear_stack:
            rpncalc.util.clear_stack()
        if len(ans) == 1:
            ans = ans[0]
        print(ans)
        return ans

    def test_numerals(self):
        expr = "1 1e3 1.01"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans[0], 1)
        self.assertEqual(ans[1], 1000)
        self.assertEqual(ans[2], 1.01)

    def test_basic_addition(self):
        expr = "1 1 + 2 +"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans, 4)

    def test_constants(self):
        expr = "pi e -"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans, numpy.pi - numpy.e)

    def test_powers(self):
        expr = "2 8 ^"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans, 256)

    def test_atan2(self):
        expr = "100000 1 atan2 pi 2 / -"
        ans = self.run_from_expr(expr)
        self.assertAlmostEqual(ans, 0, 4)

    def test_cross_product(self):
        expr = "e_x e_y cross e_z - norm"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans, 0)

    def test_determinant(self):
        expr = "1 2 3 4 matsq det"
        ans = self.run_from_expr(expr)
        self.assertAlmostEqual(ans, -2)

    def test_storage_retrieval(self):
        expr = "1 store_x _x"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans, 1)

    def test_matrix_square(self):
        expr = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 matsq"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans.shape, (4, 4))

    def test_matrix_reshape(self):
        expr = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 matsq 8 2 reshape"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans.shape, (8, 2))

    def test_vector_norm(self):
        expr = "1 2 3 vec3 norm"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans, numpy.sqrt(14))

    def test_matrix_mult(self):
        expr = (
            "1 3 5 7 11 13 15 17 23 matsq store_A "
            "1 3 5 vec3 store_b _A _b dot"
            )
        ans = self.run_from_expr(expr)
        ans = ans.flatten()
        self.assertTrue(all(ans == [35, 105, 181]))

    def test_stacking(self):
        expr = (
            "1 3 5 7 11 13 15 17 23 matsq store_A "
            "1 3 5 vec3 store_b _A _b dot"
            )
        ans = self.run_from_expr(expr, clear_stored=False)
        expr = "1 3 5 vec3 7 11 13 vec3 15 17 23 vec3 hstack hstack _A T - sum"
        ans = self.run_from_expr(expr)
        self.assertEqual(ans, 0)

    def test_matrix_solve(self):
        expr = "2 1 1 1 2 1 1 3 3 matsq inv 13 11 19 vec3 dot"
        ans = self.run_from_expr(expr)
        ans = ans.flatten()
        self.assertAlmostEqual(ans[0], 4)
        self.assertAlmostEqual(ans[1], 2)
        self.assertAlmostEqual(ans[2], 3)

    def test_help(self):
        # Test if calling help string crashes or not.
        # Different codepath for constants
        self.run_from_expr("help_mu0")
        self.run_from_expr("help_T")


if __name__ == '__main__':
    unittest.main()
