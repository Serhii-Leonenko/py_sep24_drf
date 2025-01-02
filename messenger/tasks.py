import time

from celery import shared_task

from messenger.models import Message


@shared_task
def count_messages():
    print("Sleeping.....")
    time.sleep(10)
    print("Counting messages")
    number_messages = Message.objects.count()
    print(f"Number of messages: {number_messages}")

    return number_messages
