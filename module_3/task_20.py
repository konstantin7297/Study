"""
Задача - Параллельная обработка числовых данных
разработайте программу, которая выполняет следующие шаги:

Сбор данных:
Создайте функцию generate_data(n), которая генерирует список из n случайных целых чисел
в диапазоне от 1 до 1000. Например, generate_data(1000000) должна вернуть список из 1
миллиона случайных чисел.

Обработка данных:
Напишите функцию process_number(number), которая выполняет вычисления над числом.
Например, вычисляет факториал числа или проверяет, является ли число простым.
Обратите внимание, что обработка должна быть ресурсоёмкой, чтобы продемонстрировать
преимущества мультипроцессинга.

Параллельная обработка:
Используйте модули multiprocessing и concurrent.futures для параллельной обработки
списка чисел.

Реализуйте три варианта:
Вариант А: Использование пула потоков с concurrent.futures.
Вариант Б: Использование multiprocessing.Pool с пулом процессов, равным количеству CPU.
Вариант В: Создание отдельных процессов с использованием multiprocessing.Process и
очередей (multiprocessing.Queue) для передачи данных.

Сравнение производительности:
Измерьте время выполнения для всех вариантов и сравните их с однопоточным
(однопроцессным) вариантом. Представьте результаты в виде таблицы или графика.

Сохранение результатов:
Сохраните обработанные данные в файл (например, в формате JSON или CSV).
"""
import csv
import functools
import random
import math
import multiprocessing as mp
from time import time
from concurrent.futures import ThreadPoolExecutor


def time_work(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        write_csv((func.__name__, time() - start))
        return result
    return wrapped


def generate_data(n: int) -> list:
    """ Создает список из n чисел в диапазоне 1 - 1000 """
    return [random.randint(1, 1001) for _ in range(n)]


def process_number(number: int = None, que: mp.Queue = None):
    """ Проводит какие-то вычисления: факториал """
    if que:
        while True:
            item = que.get()
            if item is None:
                break
            math.factorial(item)
    else:
        math.factorial(number)


def write_csv(row: tuple):
    with open('task_20_result.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(row)


@time_work
def variant_default(data: list):
    """ Вариант без всего. """
    for num in data:
        process_number(num)


@time_work
def variant_a(data: list):
    """ Вариант А: Использование пула потоков с 'concurrent.futures'. """
    with ThreadPoolExecutor(max_workers=mp.cpu_count()) as executor:
        futures = [executor.submit(process_number, num, None) for num in data]

        for future in futures:
            future.result()


@time_work
def variant_b(data: list):
    """ Вариант Б: Использование 'multiprocessing.Pool' с пулом процессов, равным количеству CPU. """
    with mp.Pool(processes=mp.cpu_count()) as pool:
        processes = [pool.apply_async(process_number, (num,)) for num in data]

        for process in processes:
            process.wait()


@time_work
def variant_c(data: list):
    """ Вариант В: Создание отдельных процессов с использованием 'multiprocessing.Process' и очередей (multiprocessing.Queue) для передачи данных. """
    queue = mp.Queue()

    processes = [
        mp.Process(target=process_number, kwargs={"que": queue})
        for _ in range(mp.cpu_count())
    ]

    for process in processes:
        process.start()

    for val in data + [None for _ in range(mp.cpu_count())]:
        queue.put(val)

    for process in processes:
        process.join()

    queue.close()


if __name__ == '__main__':
    numbers = generate_data(10000)
    for variant in [variant_default, variant_a, variant_b, variant_c]:
        variant(data=numbers)
