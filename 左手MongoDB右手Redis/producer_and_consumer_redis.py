import time
import json
import random
from threading import Thread

import redis


class Producer(Thread):
    def __init__(self):
        super().__init__()
        self.queue = redis.Redis()

    def run(self):
        while True:
            a = random.randint(0, 10)
            b = random.randint(90, 100)
            print(f'消费者生产了两个数值：{a}, {b}')
            self.queue.rpush('producer', json.dumps((a, b)))
            time.sleep(2)
