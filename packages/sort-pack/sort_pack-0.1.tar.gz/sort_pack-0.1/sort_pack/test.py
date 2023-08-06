"""Модуль, содержащий тесты"""
from sort_counting import sort_list


class TestClass:
    """Класс запуска тестов"""

    def test_one(self):
        """Первый тест"""
        assert sort_list(list_not_sort=[]) == []

    def test_two(self):
        """Второй тест"""
        assert sort_list([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

    def test_three(self):
        """Третий тест"""
        assert sort_list([0, -3, 3, -5, 10]) == [-5, -3, 0, 3, 10]

    def test_four(self):
        """Четвёртый тест"""
        assert sort_list([1]) == [1]

    def test_five(self):
        """Пятый тест"""
        assert sort_list(list(range(9, 0, -1))) == list(range(1, 10))


