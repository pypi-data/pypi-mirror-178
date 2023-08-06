from ..listfunc.funcs import selection_sort


class TestClass:
    def test_one(self):
        assert selection_sort([]) == []

    def test_two(self):
        assert selection_sort([6, 5, 4, 3, 2, 1, ]) == [1, 2, 3, 4, 5, 6]

    def test_three(self):
        assert selection_sort([6, 6, 6, 5, 5, 5, 4, 4, 4, 100, 100, 100]) \
               == [4, 4, 4, 5, 5, 5, 6, 6, 6, 100, 100, 100]

    def test_four(self):
        assert selection_sort([1, 2, 3, 4, 5, 5]) == [1, 2, 3, 4, 5, 5]

    def test_five(self):
        assert selection_sort([0, 0, 0, 0, 0] + [999] * 123 + [666] * 321) \
               == [0, 0, 0, 0, 0] + [666] * 321 + [999] * 123
