"""Воробьев Леонид, КИ22-16/1б, практическая работа 4, варинат 10"""


import argparse
from find_palindrom import do_iterations
from pytest import main as pytest


def main():
    '''Накопление аргументов из коммандной строки,
    демонстрация работы функции/тест функции
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', type=int,
                        help='Число, с которого начинается перебор')
    parser.add_argument('-f', '--finish', type=int,
                        help='Число, до которого будет происходить перебор')
    parser.add_argument('-m', '--МахIterations', type=int,
                        help='Максимальное число итераций, во время создания палиндрома')
    parser.add_argument('-t', '--test', type=bool,
                        action=argparse.BooleanOptionalAction, help='Запустить тест')
    args = parser.parse_args()
    start = args.start
    finish = args.finish
    maxiter = args.МахIterations
    test = args.test

    if test:
        if any([start, finish, maxiter]):
            print('Тестовый режим не использвует вводимые параметры')
        pytest(['-q', 'find_palindroms/__test__.py'])
        return
    if not any([start, finish, maxiter]):
        print('Отсутствуют входные данные')
    elif not finish:
        print('"-f" - это обязательный параметр')
    elif all([start, maxiter]):
        print(do_iterations(start, maxiter, finish))
    elif not any([start, maxiter]):
        print(do_iterations(b=finish))
    elif start:
        print(do_iterations(a=start, b=finish))
    else:
        print(do_iterations(iterations=maxiter, b=finish))


if __name__ == '__main__':
    main()
