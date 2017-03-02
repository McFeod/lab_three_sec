from functools import partial

import math

from sympy import gcdex
from sympy.ntheory import randprime

from abstractions import Keygen

MIN_RANDOM = 0x10000000  # границы для p и q
MAX_RANDOM = 0xffffffff
SYMBOL_SIZE = 8          # максимальный размер n (модуля) в байтах
get_random_prime = partial(randprime, MIN_RANDOM, MAX_RANDOM)


def euler(p, q):
    return (p - 1) * (q - 1)


def closest_fermat_number(num):
    """
    Поиск ближайшего снизу числа Ферма
    """
    return 2**int(math.log2(num)) + 1


def find_exponent(num):
    """
    Для поиска открытой экспоненты воспользуемся числами Ферма
    :param num: верхняя граница поиска
    :return: число, взаимно простое с num
    """
    e = closest_fermat_number(num)
    while math.gcd(num, e) != 1:
        e = closest_fermat_number(int(e / 2))
    return e


class RsaKeygen(Keygen):
    def generate_key(self):
        """
        Генерация RSA-ключа
        :return: кортеж из открытой и закрытой частей
        """
        p = get_random_prime()      # инициализация
        q = get_random_prime()
        n = p * q                   # модуль
        phi = euler(p, q)           # функция Эйлера
        e = find_exponent(phi)      # открытая экспонента
        public_key = (e, n)         # открытый ключ
        d, _, gcd = gcdex(e, phi)  # уравнение Евклида
        assert gcd == 1
        d = int((d + phi) % phi)    # секретная экспонента
        private_key = (d, n)        # закрытый ключ
        self.steps = locals()
        return public_key, private_key
