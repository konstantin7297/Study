"""
Задача - Декоратор кеширования
Реализуйте декоратор, согласно следующим требованиям

Этот декоратор должен кешировать результаты вызовов функции на основе её аргументов.
Если функция вызывается с теми же аргументами, что и ранее, возвращайте результат из кеша вместо повторного выполнения функции.
Реализуйте кеширование с использованием словаря, где ключами будут аргументы функции, а значениями — результаты её выполнения.
Ограничьте размер кеша до 100 записей. При превышении этого лимита удаляйте наиболее старые записи (используйте подход FIFO).
"""
import functools
from collections import OrderedDict


def cache(func, maxsize: int = 100):
    """ Декоратор кэширования. """
    cache_list = OrderedDict()
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if check_cache := cache_list.get(args, None):
            return check_cache

        result = func(*args, **kwargs)

        cache_list[args] = result
        if len(cache_list.keys()) >= maxsize + 1:
            cache_list.popitem(last=False)

        return result
    return wrapper
