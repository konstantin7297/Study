"""
Задача - Ограничитель скорости (Rate Limiter)

Ваше приложение делает HTTP запросы в сторонний сервис (функция `make_api_request`), при
этом сторонний сервис имеет проблемы с производительностью и ваша
задача ограничить количество запросов к этому сервису - не больше пяти запросов за
последние три секунды.

Ваша задача реализовать `RateLimiter.test` метод который:
1. возвращает True в случае если лимит на кол-во запросов не достигнут
2. возвращает False если за последние 3 секунды уже сделано 5 запросов.

Ваша реализация должна использовать Redis, т.к. предполагается что приложение работает
на нескольких серверах.
"""
import random
from datetime import timedelta

import redis
import time


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    redis_client = redis.Redis()
    max_calls: int = 5
    period: timedelta = timedelta(seconds=3)

    def test(self) -> bool:
        current_count = self.redis_client.incr("key")
        if current_count == 1:
            self.redis_client.expire("key", self.period)
        return current_count <= self.max_calls


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    success, failed = 0, 0

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
