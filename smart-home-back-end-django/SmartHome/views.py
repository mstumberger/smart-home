# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from rest_framework import viewsets

from SmartHome.models import Client, Dashboard, Sensor
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from SmartHome.serializers import DashboardSerializer, SensorSerializer, ClientSerializer


@csrf_exempt
def clients(request):
    return HttpResponse(json.dumps("data"), content_type='application/json')
    """ Retrieve a client config from DB and send it back to the client """
    ip = request.POST.get('ip', None)
    try:
        client, created = Client.objects.get_or_create(ip=ip)
        data = model_to_dict(client)
    except Exception as e:
        print("Could not retrieve client config for IP '{}': {}".format(ip, e))
    else:
        print("Client config for retrieved for IP '{}'".format(ip, data))
        return HttpResponse(json.dumps(data), content_type='application/json')


# ViewSets define the view behavior.
class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# ViewSets define the view behavior.
class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


# ViewSets define the view behavior.
class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

