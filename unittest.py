import unittest
from main import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_positive_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_negative_integers(self):
        self.assertEqual(add_numbers(-2, -3), -5)

    def test_mixed_sign_integers(self):
        self.assertEqual(add_numbers(-2, 3), 1)

    def test_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(0, 5), 5)
        self.assertEqual(add_numbers(5, 0), 5)

    def test_floats(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.1), 5.6)
        self.assertAlmostEqual(add_numbers(-2.5, 2.5), 0.0)

    def test_large_numbers(self):
        self.assertEqual(add_numbers(1_000_000, 2_000_000), 3_000_000)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            add_numbers("2", 3)
        with self.assertRaises(TypeError):
            add_numbers(None, 3)

if __name__ == "__main__":
    unittest.main()