"""
Модуль содержить функцию sort_list, сортирующий список методом подсчёта
"""


def sort_list(list_not_sort):
    """
    Функция, сортирующая список методом слияния
    Пример работы функции:
    >>> sort_list([4, 5, -1, 6, 4, -10, 11])
    [-10, -1, 4, 4, 5, 6, 11]
    >>> sort_list([4, 5, 7, 1, 9, 0])
    [0, 1, 4, 5, 7, 9]
    """
    list_sort = []
    if not list_not_sort:
        return []
    for element in range(min(list_not_sort), max(list_not_sort) + 1):
        if element in list_not_sort:
            list_sort.extend([element] * list_not_sort.count(element))
    return list_sort


if __name__ == '__main__':
    import doctest
    doctest.testmod()
