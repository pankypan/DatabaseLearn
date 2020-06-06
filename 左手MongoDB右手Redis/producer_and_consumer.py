import time
import random
from queue import Queue
from threading import Thread


class Producer(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            a = random.randint(0, 10)
            b = random.randint(90, 100)
            print(f'生产者产生了两个数值: {a}, {b}')
            self.queue.put((a, b))
            time.sleep(2)


class Consumer(Thread):
    def __init__(self, queue, thread_id):
        super().__init__()
        self.queue = queue
        self.thread_id = thread_id

    def run(self):
        while True:
            num_tuple = self.queue.get(block=True)  # block=True 表示，如果队列为空则阻塞在这里，直到有数据为止
            sum_a_b = sum(num_tuple)
            print(f'消费者{self.thread_id}消费了一组数：{num_tuple[0]} + {num_tuple[1]} = {sum_a_b}')
            # time.sleep(random.randint(0, 10))
            time.sleep(1)


queue = Queue()
producer = Producer(queue)
consumer1 = Consumer(queue, 1)
consumer2 = Consumer(queue, 2)

producer.start()
consumer1.start()
consumer2.start()
