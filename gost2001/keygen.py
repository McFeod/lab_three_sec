from functools import partial
from random import randint

from sympy import randprime, sqrt_mod_iter, isprime
from gost2001.ecc import mul, add
from utils.utils import positive_mod

MIN_RANDOM = 0x1000  # границы n
MAX_RANDOM = 0xffff
COEFFICIENT_RANGE = 0xff     # граница для a, b
get_random_prime = partial(randprime, MIN_RANDOM, MAX_RANDOM)
get_coefficient = partial(randint, 1, COEFFICIENT_RANGE)


def check_q(q, n):
    """
    Проверка ограничений для ранга цикличекой подкруппы

    """
    if isprime(q):
        for i in range(2, 12):
            if pow(n, i, q) == 1:
                break
        else:
            return True
    return False


def check_coefficients(a, b, n):
    """
    Проверка кривой ``y^2 = x^3 + a*x + b (mod n)`` на гладкость.
    :return: True, если кривая является гладкой
    """
    return (4 * pow(a, 3, n) + 27 * pow(b, 2, n)) % n != 0


def generate_coefficients():
    """
    Подбор случайных коэффициентов для получения гладкой эллиптической кривой
    ``y^2 = x^3 + a*x + b (mod n)``
    :return: a, b, n
    """
    n = get_random_prime()
    a = get_coefficient()
    b = get_coefficient()
    return a, b, n if check_coefficients(a, b, n) else generate_coefficients()


def get_random_point(a, b, n):
    """
    Получение случайной точки на эллиптической кривой ``y^2 = x^3 + a*x + b (mod n)``
    :return: Точка (x, y)
    """
    success = False
    while not success:
        try:
            x = randint(1, n)
            y = next(sqrt_mod_iter(positive_mod(pow(x, 3, n) - (a * x) - b, n), n))
            return x, y
        except StopIteration:
            pass


def find_rank(point, curve):
    """
    Определение числа точек в группе на кривой
    :param point: начальная точка
    :param curve: параметры кривой
    :return: число точек (q)
    """
    last_point = add(point, point, curve)
    total_count = 3  # 2 точки посчитано + точка O

    while last_point[0] != point[0]:
        total_count += 1
        last_point = add(last_point, point, curve)
    return total_count


class Gost2001Keygen:
    steps = None

    def generate_key(self):
        a, b, n = generate_coefficients()
        x_p, y_p = get_random_point(a, b, n)
        q = find_rank((x_p, y_p), (a, b, n))
        if not check_q(q, n):
            print('q is not suitable')
            return self.generate_key()
        d = randint(1, q)
        x_q, y_q = mul((x_p, y_p), d, (a, b, n))
        private_key = d
        public_key = ((a, b, n), (x_p, y_p), q, (x_q, y_q))
        self.steps = locals()
        return public_key, private_key

if __name__ == '__main__':
    keygen = Gost2001Keygen()
    print(keygen.generate_key())
