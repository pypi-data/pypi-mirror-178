'''Тесты функции do_iterations'''


from find_palindrom import do_iterations


class TestClass:
    def test_one(self):
        assert do_iterations() == [(0, 0, 0), (1, 1, 0), (2, 2, 0), (3, 3, 0), (
            4, 4, 0), (5, 5, 0), (6, 6, 0), (7, 7, 0), (8, 8, 0), (9, 9, 0)]

    def test_two(self):
        assert do_iterations(4, 4, 0) == []

    def test_three(self):
        assert do_iterations(0, 0, 0) == []

    def test_four(self):
        assert do_iterations(-1, -5, -6) == [(1, 1, 0),
                                             (2, 2, 0), (3, 3, 0), (4, 4, 0), (5, 5, 0)]

    def test_five(self):
        assert do_iterations(56, 5, 57) == [(56, 121, 1)]
