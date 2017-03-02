from hashlib import sha512
from random import randint

from sympy.ntheory.modular import crt

from abstractions import Prover, Verifier
from gost2001.ecc import mul, add
from utils.utils import calc_hash, positive_mod


class Gost2001Prover(Prover):
    def sign(self, message):
        """
        Создание электронной подписи
        """
        (a, b, n), (x_p, y_p), q, _ = self.public_key
        h = calc_hash(message, sha512)
        e = h % q
        s = k = r = 0
        while s == 0:
            while r == 0:
                k = randint(1, q - 1)
                x_c, y_c = mul((x_p, y_p), k, (a, b, n))  # умножение точки на кривой на число
                r = x_c % q
            s = (r * self._private_key + k * e) % q
        self.steps = locals()
        return r, s


class Gost2001Verifier(Verifier):
    def verify(self, message, signature):
        """
        Подтверждение авторства сообщения
        """
        (a, b, n), (x_p, y_p), q, (x_q, y_q) = self.prover_key
        r, s = signature
        h = calc_hash(message, sha512)
        e = h % q
        e_1 = int(crt((e, q), (0, 1))[0]) // e  # обратное значение
        v = e_1 % q
        z1 = (s * v) % q
        z2 = positive_mod((q - r) * v, q)
        x_c, y_c = add(
            mul((x_p, y_p), z1, (a, b, n)),
            mul((x_q, y_q), z2, (a, b, n)),
            (a, b, n))
        r_ = x_c % q
        passed = r == r_
        self.steps = locals()
        return passed
