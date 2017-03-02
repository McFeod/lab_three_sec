from abc import abstractmethod, ABC


class Prover(ABC):
    def __init__(self, keys):
        self.public_key, self._private_key = keys
        self.steps = None

    @abstractmethod
    def sign(self, message):
        pass


class Verifier(ABC):
    def __init__(self, public_key):
        self.prover_key = public_key
        self.steps = None

    @abstractmethod
    def verify(self, message, signature):
        pass


class Keygen(ABC):
    steps = None   # хранение промежуточных вычислений для отчёта

    @abstractmethod
    def generate_key(self):
        pass
