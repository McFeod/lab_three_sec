from functools import partial
from random import randint

from sympy import primitive_root
from sympy.ntheory import randprime
from sympy.ntheory.factor_ import smoothness

MIN_RANDOM = 0x10000000  # границы для p и q
MAX_RANDOM = 0xffffffff
get_random_prime = partial(randprime, MIN_RANDOM, MAX_RANDOM)


def find_root(p, q):
    """
    Быстрый аналог _nthroot_mod1 из sympy для случая s=1, all_roots=False
    """
    return (pow(primitive_root(p), (p - 1) // q, p)) % p


class Gost94Keygen:
    steps = None

    def generate_key(self):
        """
        Генерация ключа для ГОСТ 30.10-94
        :return: открытый и закрытый ключ
        """
        p = get_random_prime()
        q = smoothness(p - 1)[0]            # максимальный простой делитель
        a = find_root(p, q)
        x = randint(1, q-1)                 # закрытый ключ
        y = pow(a, x, p)                    # открытый ключ
        public_key = (p, q, a, y)
        private_key = x
        self.steps = locals()
        return public_key, private_key
