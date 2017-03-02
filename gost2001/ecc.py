from sympy.ntheory.modular import crt

from utils.utils import positive_mod


def find_lambda(numerator, denominator, n):
    """
    Вычисление значения l = numerator/denominator (mod n)
    :return: l
    """
    left = positive_mod(denominator, n)
    right = positive_mod(numerator, n)
    return int(crt((left, n), (0, right))[0] // left)


def add(first, second, curve):
    """
    Операция сложения над точками кривой
    :param first: первая точка
    :param second: вторая точка
    :param curve: параметры кривой
    :return: новая точка
    """
    if first == (0, 0):
        return second
    if second == (0, 0):
        return first
    x1, y1 = first
    x2, y2 = second
    if x1 == x2 and y1 != y2:
        return 0, 0
    a, b, n = curve
    if x1 == x2:
        l = find_lambda(3 * x1 * x1 + a, 2 * y1, n)
    else:
        l = find_lambda(y2 - y1, x2 - x1, n)
    x = positive_mod(l * l - x1 - x2, n)
    y = positive_mod(l * (x1 - x) - y1, n)
    return x, y


def mul(point, factor, curve):
    """
    Операция умножения над точками кривой
    :param point: точка
    :param factor: множитель-число
    :param curve: параметры кривой
    :return: новая точка
    """
    result = (0, 0)
    temp = point
    while 0 < factor:
        if factor & 1 == 1:
            result = add(result, temp, curve)
        factor, temp = factor >> 1, add(temp, temp, curve)
    return result
