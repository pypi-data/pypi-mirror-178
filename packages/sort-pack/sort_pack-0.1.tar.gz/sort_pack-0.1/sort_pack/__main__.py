import argparse as args  #
from random_list import generation_list
from sort_counting import sort_list
from pytest import main as pytest


def main_():
    """
    Главная функция, запускающая всю программу
    и обрабатывающая параметры CLI
    :return: None
    """
    parser = args.ArgumentParser()
    parser.add_argument('--list', '-l', type=int, help='Введите массив', nargs='+')
    parser.add_argument('--rand', '-r', type=int, help='Введите число элементов')
    parser.add_argument('--test', '-t', type=bool, action=args.BooleanOptionalAction,
                        help='Введите для запуска теста')
    arg = parser.parse_args()
    if arg.test:
        print("Начинаем запуск тестов")
        pytest(['sort_pack/test.py', '-v'])
        return
    elif not (arg.list or arg.rand):
        print('Ни один из параметров не введён')
    elif arg.list and not arg.rand:
        print(sort_list(arg.list))
    elif (not arg.list) and arg.rand:
        print('Создан случайный список:')
        print(rand := generation_list(arg.rand))
        print(sort_list(rand))
    elif arg.list and arg.rand:
        print('Введите только один параметр')


if __name__ == '__main__':
    main_()
