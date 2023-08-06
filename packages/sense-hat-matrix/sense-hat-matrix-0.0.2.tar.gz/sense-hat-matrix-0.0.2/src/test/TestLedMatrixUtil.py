import unittest

import LedMatrixUtil
import PrettyPrint


o = [0, 0, 0]  # Black
R = [255, 0, 0]  # Red
G = [0, 255, 0]  # Green


class LedMatrixUtilSpec(unittest.TestCase):

    def test_should_make_matrix_from_list(self):
        name_of_test = "should_make_matrix_from_list"
        result = LedMatrixUtil.list_to_matrix([
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R,
            o, o, o, o, o, o, o, R
            ])
        PrettyPrint.pretty_print(name_of_test, result)
        assert result == [
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R]
            ], name_of_test

    def test_should_left_shift_matrix_by_one(self):
        name_of_test = "should_left_shift_matrix_by_one"
        matrix = [
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R],
            [o, o, o, o, o, o, o, R]
            ]
        result = LedMatrixUtil.shift_matrix_to_left(matrix)
        PrettyPrint.pretty_print(name_of_test, result)
        assert result == [
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o],
            [o, o, o, o, o, o, R, o]
            ], name_of_test


if __name__ == "__main__":
    unittest.main()
