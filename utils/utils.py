def numbers_to_bytes(numbers, size):
    """
    Перевод чисел в байты
    :param numbers: список целых чисел
    :param size: максимальный размер числа в байтах
    :return: объект bytes
    """
    return b"".join(x.to_bytes(size, 'big') for x in numbers)


def bytes_to_numbers(message, size):
    """
    Преобразование набора байт в список чисел
    :param message: исходные данные
    :param size: размер одного числа в байтах
    :return: список целых чисел
    """
    return [int.from_bytes(message[x: x + size], 'big') for x in range(0, len(message), size)]


def use_cp1251(func):
    def wrapper(data, *args, **kwargs):
        return func(data.encode('cp1251'), *args, **kwargs)
    return wrapper


def positive_mod(x, n):
    return (x + n) % n


@use_cp1251
def calc_hash(message, func):
    return int.from_bytes(func(message).digest(), 'big')
