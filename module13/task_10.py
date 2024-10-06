"""
Задача - Распределенный лок
У вас есть распределенное приложение работающее на десятках серверах. Вам необходимо
написать декоратор single который гарантирует, что декорируемая функция не исполняется
параллельно.

Параметр max_processing_time указывает на максимально допустимое время работы
декорируемой функции.
"""
import datetime
import functools
import redis
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

redis_client = redis.Redis(host='localhost', port=6379, db=0)


def single(max_processing_time: datetime.timedelta = datetime.timedelta(minutes=1)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            max_run_time = int(max_processing_time.total_seconds())
            if redis_client.set(func.__name__, "locked", nx=True, ex=max_run_time):
                try:
                    return func(*args, **kwargs)
                finally:
                    redis_client.delete(func.__name__)
            else:
                raise RuntimeError(f"Функция {func.__name__!r} уже запущена.")
        return wrapper
    return decorator


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    time.sleep(2)


if __name__ == '__main__':
    """
    Зависимости: 
        sudo apt-get install redis-server 
        pip install requirements.txt
    count:
        1 - Все ок.
        2 - Вызывает ошибку.
    """
    count = 2

    with ThreadPoolExecutor(max_workers=count) as executor:
        threads = [executor.submit(process_transaction,) for _ in range(count)]

        for thread in as_completed(threads):
            thread.result()

    print('Все ок.')
