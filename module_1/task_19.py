"""
Задача - Декоратор кеширования:
Реализуйте декоратор, согласно следующим требованиям

Этот декоратор должен кешировать результаты вызовов функции на основе её аргументов.
Если функция вызывается с теми же аргументами, что и ранее, возвращайте результат из кеша вместо повторного выполнения функции.
Реализуйте кеширование с использованием словаря, где ключами будут аргументы функции, а значениями — результаты её выполнения.
Ограничьте размер кеша до 100 записей. При превышении этого лимита удаляйте наиболее старые записи (используйте подход FIFO).
"""
import functools
import unittest
from collections import OrderedDict
from unittest.mock import MagicMock


def cache(maxsize: int = 100):
    """ Декоратор кэширования. """
    cache_list = OrderedDict()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if check_cache := cache_list.get((args, frozenset(kwargs.items()))):
                return check_cache

            result = func(*args, **kwargs)
            cache_list[(args, frozenset(kwargs.items()))] = result
            if len(cache_list) == maxsize + 1:
                cache_list.popitem(last=False)

            return result
        return wrapper
    return decorator


class TestCacheDecorator(unittest.TestCase):
    def test_cache_args_kwargs(self):
        """ Проверка с args и kwargs """
        mock_func = MagicMock(return_value=111)
        decorated_func = cache(100)(mock_func)

        decorated_func(1, 2, a=3, b=4)
        result = decorated_func(1, 2, a=3, b=4)
        assert result == 111
        assert mock_func.call_count == 1

    def test_cache_maxsize(self):
        """ Проверка maxsize """
        mock_func = MagicMock(return_value=111)
        decorated_func = cache(1)(mock_func)

        decorated_func(1, a=2)  # Создаем кэш, функция выполняется.
        decorated_func(2, a=3)  # Заменяем кэш, функция выполняется.
        decorated_func(1, a=2)  # Кэш заполнен, снова функция выполняется.

        assert mock_func.call_count == 3  # Функция вызывается 3 раза, т.е. кэша не было
