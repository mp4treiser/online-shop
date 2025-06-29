from celery import shared_task
@shared_task
def debug_task(x):
    s = f"hwllo world {x}"
    print(s)
    return s