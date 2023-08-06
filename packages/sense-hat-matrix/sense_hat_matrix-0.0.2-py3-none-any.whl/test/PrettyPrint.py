import LedMatrixUtil


def pretty_print_list(name_of_test, list_of_matrix):
    matrix = LedMatrixUtil.list_to_matrix(list_of_matrix)
    pretty_print(name_of_test, matrix)


def pretty_print(name_of_test, matrix):
    print(name_of_test)
    for row in matrix:
        line = ""
        for c in row:
            line += str(c)
            line += ",\t\t"
        print(line)


def debug_pretty_print(expected, actual):
    if len(expected) != len(actual):
        print("Number of rows are not the same of expected [" + len(expected) + "] and actual [" + len(actual) + "]")
    if len(expected[0]) != len(actual[0]):
        print("Number of columns are not the same of expected [" + len(expected[0]) + "] and actual [" + len(actual[0]) + "]")

    for r in range(0, len(expected)):
        line = ""
        for c in range(0, len(expected[r])):
            e = expected[r][c]
            a = actual[r][c]
