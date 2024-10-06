"""
Задача - Очередь
Реализуйте класс который реализует следующий протокол:
"""
import typing


class RedisQueue(typing.Protocol):
    def publish(self, msg: dict):
        """ Публикация """

    def consume(self) -> dict:
        """ Потребление """

