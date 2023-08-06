
from LedMatrixUtil import MatrixType
from LedMatrixUtil import ListType
from LedMatrixUtil import list_to_matrix
from LedMatrixUtil import matrix_to_list
from LedMatrixUtil import shift_matrix_to_left
from LedMatrixUtil import set_column


# LED Matrix assumes an 8 x 8 LED panel which you can find on the pi's sense-hat
class LedMatrix:
    matrix: MatrixType

    def __init__(self):
        O = [0, 0, 0]  # Black
        self.matrix = list_to_matrix([
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O,
            O, O, O, O, O, O, O, O
        ])

    def add_column_to_right(self, column) -> None:
        self.matrix = shift_matrix_to_left(self.matrix)
        self.matrix = set_column(self.matrix, 7, column)

    def render(self) -> ListType:
        return matrix_to_list(self.matrix)
