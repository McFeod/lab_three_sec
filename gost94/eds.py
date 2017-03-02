from hashlib import sha256
from random import randint

from abstractions import Prover, Verifier
from utils.utils import positive_mod, calc_hash


class Gost94Prover(Prover):
    def sign(self, message):
        """
        Подтверждение авторства сообщения
        """
        p, q, a, y = self.public_key
        h = calc_hash(message, sha256)
        s = w_ = w = k = 0
        while s == 0:
            while w == 0:
                k = randint(1, q)
                w = pow(a, k, p)
                w_ = w % q
            s = positive_mod(self._private_key * w_ + k * h, q)
        self.steps = locals()
        return w_, s


class Gost94Verifier(Verifier):
    def verify(self, message, signature):
        p, q, a, y = self.prover_key
        w, s = signature
        h = calc_hash(message, sha256)
        v = pow(h, q-2, q)
        z1 = positive_mod(s * v, q)
        z2 = positive_mod((q - w) * v, q)
        u = positive_mod(positive_mod(pow(a, z1, p) * pow(y, z2, p), p), q)
        passed = w == u
        self.steps = locals()
        return passed
