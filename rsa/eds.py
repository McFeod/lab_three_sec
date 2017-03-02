from hashlib import md5

from abstractions import Prover, Verifier
from utils.utils import calc_hash


class RsaProver(Prover):
    def sign(self, message):
        h = calc_hash(message, md5)
        s = pow(h, *self._private_key)
        self.steps = locals()
        return s


class RsaVerifier(Verifier):
    def verify(self, message, signature):
        h1 = calc_hash(message, md5)
        h2 = pow(signature, *self.prover_key)
        passed = h1 % self.prover_key[1] == h2
        self.steps = locals()
        return passed
