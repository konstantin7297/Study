"""
Задача - Декоратор кеширования
Реализуйте декоратор, согласно следующим требованиям

Этот декоратор должен кешировать результаты вызовов функции на основе её аргументов.
Если функция вызывается с теми же аргументами, что и ранее, возвращайте результат из кеша вместо повторного выполнения функции.
Реализуйте кеширование с использованием словаря, где ключами будут аргументы функции, а значениями — результаты её выполнения.
Ограничьте размер кеша до 100 записей. При превышении этого лимита удаляйте наиболее старые записи (используйте подход FIFO).
"""
import functools
import unittest
from collections import OrderedDict


def cache(maxsize: int = 100):
    """ Декоратор кэширования. """
    def decorator(func):
        cache_list = OrderedDict()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if check_cache := cache_list.get((args, frozenset(kwargs.items()))):
                return check_cache

            result = func(*args, **kwargs)
            cache_list[(args, frozenset(kwargs.items()))] = result
            if len(cache_list) >= maxsize + 1:
                cache_list.popitem(last=False)

            return result
        return wrapper
    return decorator


class TestCacheDecorator(unittest.TestCase):
    def test_with_args(self):
        """ Работа с args """
        @cache(maxsize=5)
        def add(a, b):
            return a + b

        result1 = add(2, 3)
        result2 = add(2, 3)
        self.assertEqual(result1, result2)
        self.assertEqual(result1, 5)

    def test_with_kwargs(self):
        """ Работа с kwargs """
        @cache(maxsize=5)
        def add(a, b, c=None):
            return a + b + (c or 0)

        result = add(1, 2, c=3)
        self.assertEqual(result, 6)
