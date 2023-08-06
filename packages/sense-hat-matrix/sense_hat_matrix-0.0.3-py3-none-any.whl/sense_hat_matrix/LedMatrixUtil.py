
import numpy as np

ListType = list[list[float]]
MatrixType = list[list[list[float]]]


def list_to_matrix(list_as_matrix: ListType) -> MatrixType:
    #         0   1   2   3   4   5   6   7
    matrix = [[], [], [], [], [], [], [], []]
    for r in range(0, 8):
        temp_array = []
        for c in range(0, 8):
            if r == 0:
                index = c
            else:
                index = r * 8 + c
            temp_array.append(list_as_matrix[index])
        matrix[r] = temp_array
    return matrix


def matrix_to_list(matrix: MatrixType) -> ListType:
    list_as_matrix = []
    for row in matrix:
        for e in row:
            list_as_matrix.append(e)
    return list_as_matrix


def shift_matrix_to_left(matrix: MatrixType) -> MatrixType:
    o = [0, 0, 0]  # Black
    for r in range(0, len(matrix)):
        matrix[r] = __shift_array(matrix[r], o)
    return matrix


def set_column(matrix: MatrixType, column_index: int, column: ListType):
    for r in range(0, len(matrix)):
        matrix[r][column_index] = column[r]
    return matrix


def __shift_array(array, default):
    size = len(array)
    for i in range(0, size):
        if i == size - 1:
            temp = default
        else:
            temp = array[i+1]
        array[i] = temp
    return array
