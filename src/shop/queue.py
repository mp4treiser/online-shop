from shop.models import Queue


class QueueService:
    FIFO = "FIFO"
    LIFO = "LIFO"
    STRATEGIES = [FIFO, LIFO]

    def __init__(self, strategy: str = FIFO):
        if strategy not in self.STRATEGIES:
            raise TypeError("Недопустимая стратегия")
        self.strategy = strategy

    def add(self, value):
        Queue.objects.get_or_create(value=value)

    def pop(self):
        if self.strategy == self.FIFO:
            item = Queue.objects.order_by("id").first()  # FIFO: первый вошёл — первый вышел
        else:
            item = Queue.objects.order_by("-id").first()  # LIFO: последний вошёл — первый вышел

        if item:
            value = item.value
            item.delete()
            return value
        return None

    def get_length(self):
        return Queue.objects.count()

    def get_last(self):
        last_item = Queue.objects.order_by("-id").first()
        return last_item.value if last_item else None