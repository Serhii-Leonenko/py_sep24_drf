from django.contrib import admin

from messenger.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
