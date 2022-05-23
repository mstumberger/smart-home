import django_filters
from .models import Event
from django.db import models


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'type': ['exact', ],
            'additional_data': ['exact'],
        }

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
