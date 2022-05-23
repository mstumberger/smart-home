from rest_framework import viewsets
from .serializers import EventSerializer
from .models import Event


class EventViewset(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    ordering_fields = ('added_at',)
    ordering = ('-added_at',)
