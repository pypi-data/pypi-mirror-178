import unittest

import GraphUtil

class GraphUtilSpec(unittest.TestCase):

    def test_should_rescale_less_than_min(self):
        result = GraphUtil.rescale(10, 20, 2)
        print(result)
        assert result == 1, "should_rescale_less_than_min"

    def test_should_rescale_more_than_max(self):
        result = GraphUtil.rescale(10, 20, 25)
        print(result)
        assert result == 8, "should_rescale_more_than_max"

    def test_should_rescale_min(self):
        result = GraphUtil.rescale(10, 20, 10)
        print(result)
        assert result == 1, "should_rescale_min"

    def test_should_rescale_max(self):
        result = GraphUtil.rescale(10, 20, 20)
        print(result)
        assert result == 8, "should_rescale_max"

    def test_should_rescale_middle(self):
        result = GraphUtil.rescale(10, 20, 15)
        print(result)
        assert result == 4, "should_rescale_middle"


if __name__ == "__main__":
    unittest.main()
