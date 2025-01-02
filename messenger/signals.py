from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from messenger.models import Message
from messenger.tasks import count_messages


@receiver([post_save, post_delete], sender=Message)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*message_view*")


@receiver([post_save], sender=Message)
def count_messages_after_new_created(sender, instance, **kwargs):
    count_messages.delay() # any other logic like sending emails, etc
