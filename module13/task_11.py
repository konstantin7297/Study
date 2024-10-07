"""
Задача - Очередь
Реализуйте класс который реализует следующий протокол:
"""
import json
import typing

import redis


class RedisQueue(typing.Protocol):
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    queue = "my_que"

    @classmethod
    def publish(cls, msg: dict):
        """ Публикация """
        msg_json = json.dumps(msg)
        cls.redis_conn.lpush(cls.queue, msg_json)

    @classmethod
    def consume(cls) -> typing.Union[dict, None]:
        """ Потребление """
        msg_json = cls.redis_conn.rpop(cls.queue)
        if msg_json is None:
            return None
        return json.loads(msg_json)


if __name__ == "__main__":
    RedisQueue.publish({'key': 'value'})
    RedisQueue.publish({'key2': 'value2'})

    while True:
        message = RedisQueue.consume()

        if message is None:
            break

        print(message)
