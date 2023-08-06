import unittest

from Graph import Graph
from PrettyPrint import pretty_print_list


R = [255, 0, 0]  # Red
G = [0, 255, 0]  # Green
B = [0, 0, 255]  # Blue
O = [0, 0, 0]


class GraphSpec(unittest.TestCase):

    def test_should_render_min_value(self):
        name_of_test = "should_render_min_value"
        graph = Graph(20, 40)
        result = graph.render(20)
        pretty_print_list(name_of_test, result)
        self.assertEqual(result, [
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, B
                ])

    def test_should_render_scaled_to_middle(self):
        name_of_test = "should_render_scaled_to_middle"
        graph = Graph(20, 30)
        result = graph.render(25)
        pretty_print_list(name_of_test, result)
        self.assertEqual(result, [
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, G,
                O, O, O, O, O, O, O, G,
                O, O, O, O, O, O, O, B,
                O, O, O, O, O, O, O, B
                ])

    def test_should_render_multiple_times_and_shifting_old_values_left(self):
        name_of_test = "should_render_multiple_times_and_shifting_old_values_left"
        graph = Graph(20, 30)
        graph.render(30)
        graph.render(25)
        result = graph.render(20)
        pretty_print_list(name_of_test, result)
        self.assertEqual(result, [
                O, O, O, O, O, R, O, O,
                O, O, O, O, O, R, O, O,
                O, O, O, O, O, G, O, O,
                O, O, O, O, O, G, O, O,
                O, O, O, O, O, G, G, O,
                O, O, O, O, O, G, G, O,
                O, O, O, O, O, B, B, O,
                O, O, O, O, O, B, B, B
                ])


if __name__ == "__main__":
    unittest.main()
