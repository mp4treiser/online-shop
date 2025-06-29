from django.test import TestCase
from shop.queue import QueueService

class TestUniqueQueue(TestCase):
    def setUp(self):
        self.fifo_queue = QueueService(strategy=QueueService.FIFO)
        self.lifo_queue = QueueService(strategy=QueueService.LIFO)

    # === Тесты стратегий (FIFO/LIFO) ===
    def test_fifo_strategy(self):
        self.fifo_queue.add(1)
        self.fifo_queue.add(2)
        self.assertEqual(self.fifo_queue.pop(), 1)  # Первый добавленный — первый извлечённый
        self.assertEqual(self.fifo_queue.pop(), 2)

    def test_lifo_strategy(self):
        self.lifo_queue.add(1)
        self.lifo_queue.add(2)
        self.assertEqual(self.lifo_queue.pop(), 2)  # Последний добавленный — первый извлечённый
        self.assertEqual(self.lifo_queue.pop(), 1)

    # === Тесты уникальности ===
    def test_add_duplicate(self):
        self.fifo_queue.add(1)
        self.fifo_queue.add(1)  # Дубликат не добавится
        self.assertEqual(self.fifo_queue.get_length(), 1)

    # === Тесты методов длины и последнего элемента ===
    def test_get_length_empty(self):
        self.assertEqual(self.fifo_queue.get_length(), 0)

    def test_get_length_after_add(self):
        self.fifo_queue.add(10)
        self.assertEqual(self.fifo_queue.get_length(), 1)

    def test_get_last_empty(self):
        self.assertIsNone(self.fifo_queue.get_last())

    def test_get_last_after_add(self):
        self.fifo_queue.add(10)
        self.fifo_queue.add(20)
        self.assertEqual(self.fifo_queue.get_last(), 20)

    # === Комбинированные тесты ===
    def test_pop_affects_length(self):
        self.fifo_queue.add(1)
        self.fifo_queue.pop()
        self.assertEqual(self.fifo_queue.get_length(), 0)

    def test_lifo_with_duplicates(self):
        self.lifo_queue.add(1)
        self.lifo_queue.add(1)  # Не должен быть добавлен, т.к. униален
        self.lifo_queue.add(2)
        self.assertEqual(self.lifo_queue.pop(), 2)
        self.assertEqual(self.lifo_queue.pop(), 1)
        self.assertEqual(self.lifo_queue.get_length(), 0)

    def test_fifo_multiple_elements(self):
        values = [1, 2, 3, 4]
        for v in values:
            self.fifo_queue.add(v)
        for v in values:
            self.assertEqual(self.fifo_queue.pop(), v)

    def test_lifo_multiple_elements(self):
        values = [1, 2, 3, 4]
        for v in values:
            self.lifo_queue.add(v)
        for v in reversed(values):
            self.assertEqual(self.lifo_queue.pop(), v)