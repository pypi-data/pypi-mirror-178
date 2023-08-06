"""Создает палиндромы из чисел в промежутке от a до b"""


def create_palindrom(number, iterations):
    """Алгоритм создающий палиндром из заданного числа

    Алгоритм берет входное значение (например 42), переворачивает чего (24),
    после суммирует исходное и получившееся значения (42+24),
    действия со значением повторяются, пока не будет достигнут
    заданный в параметрах лимит итераций, либо пока не получится палиндром

    :param number: Исходное значение (int)
    :param iterations: Максмимальное кол-во итераций (int)
    :return: возвращается получившийся палиндром и кол-во итераций,
    необходимое для его получения, если палиндром не получился
     - возвращается "0"
    """
    count = 0
    while str(number) != str(number)[::-1] and count < iterations:
        number += int(str(number)[::-1])
        count += 1
    if str(number) == str(number)[::-1]:
        return (number, count)
    else:
        return 0


def do_iterations(a=0, iterations=50, b=10):
    """Алгоритм создает палиндромы из чисел диапозона [a,b)
    Пример работы функции:
    >>> do_iterations(4,4,0)
    []
    >>> do_iterations(56, 5, 57)
    [(56, 121, 1)]
    """
    iterations=abs(iterations)
    palindroms = []
    for i in range(abs(a), abs(b)):
        if create_palindrom(i, iterations) != 0:
            palindroms.append((i,)+create_palindrom(i, iterations))
    return palindroms


if __name__ == '__main__':
    import doctest
    doctest.testmod()
