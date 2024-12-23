from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from messenger.models import Message


@receiver([post_save, post_delete], sender=Message)
def invalidate_message_cache(sender, instance, **kwargs):
    cache.delete_pattern("*message_view*")
