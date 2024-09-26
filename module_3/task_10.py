"""
Задача - Асинхронный HTTP-запрос
опишите асинхронную функцию fetch_urls, которая принимает список URL-адресов и
возвращает словарь, где ключами являются URL, а значениями — статус-коды ответов.
Используйте библиотеку aiohttp для выполнения HTTP-запросов.

Требования:
Ограничьте количество одновременных запросов до 5.
Обработайте возможные исключения (например, таймауты, недоступные ресурсы) и
присвойте соответствующие статус-коды (например, 0 для ошибок соединения).
"""
import asyncio
from asyncio import Semaphore

import aiohttp
from aiohttp import ClientSession


urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]


async def fetch_url(
        session: ClientSession,
        url: str,
        semaphore: Semaphore,
) -> (str, int):
    """ Функция для одиночного запроса """
    async with semaphore:
        try:
            async with session.get(url) as response:
                return url, response.status
        except aiohttp.ClientConnectionError:
            return url, 0
        except aiohttp.ClientTimeout:
            return url, 408
        except aiohttp.ClientResponseError as e:
            return url, e.status


async def fetch_urls(urls: list, request_count: int = 5) -> dict:
    """ Основная функция для строения запросов """
    async with ClientSession() as session:
        semaphore = Semaphore(request_count)
        tasks = [fetch_url(session, url, semaphore) for url in urls]
        result = await asyncio.gather(*tasks)
        return dict(result)


results = asyncio.run(fetch_urls(urls))
print(results)

# Пример вывода:
# {
#     "https://example.com": 200,
#     "https://httpbin.org/status/404": 404,
#     "https://nonexistent.url": 0
# }
