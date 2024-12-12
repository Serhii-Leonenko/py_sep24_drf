from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters


class MessageFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        queryset=get_user_model().objects.all(), to_field_name="id"
    )
