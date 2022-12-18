# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from SmartHome.models import Client, Dashboard, ConfiguredModule, GPIOPinConfig, BoardType, AVAILABLE_MODULES, \
    AvailableModule
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from SmartHome.serializers import DashboardSerializer, ModuleSerializer, ClientSerializer, GPIOPinConfigSerializer, \
    BoardTypeSerializer, ModuleWithClientSerializer, AvailableModuleSerializer


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

    @action(detail=False, methods=['get'])
    def get_used_pins(self, request: Request, pk=None):
        recent_users = ConfiguredModule.objects.all()
        serializer = ModuleSerializer(recent_users, many=True)
        return Response(serializer.data)


# ViewSets define the view behavior.
class AvailableModuleViewSet(viewsets.ModelViewSet):
    queryset = AvailableModule.objects.all()
    serializer_class = AvailableModuleSerializer


# ViewSets define the view behavior.
class ModuleViewSet(viewsets.ModelViewSet):
    queryset = ConfiguredModule.objects.all()
    serializer_class = ModuleSerializer


# ViewSets define the view behavior.
class ModuleWithClientViewSet(viewsets.ModelViewSet):
    queryset = ConfiguredModule.objects.all()
    serializer_class = ModuleWithClientSerializer


# ViewSets define the view behavior.
class GPIOPinConfigViewSet(viewsets.ModelViewSet):
    queryset = GPIOPinConfig.objects.all()
    serializer_class = GPIOPinConfigSerializer


# ViewSets define the view behavior.
class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer


# ViewSets define the view behavior.
class BoardTypeViewSet(viewsets.ModelViewSet):
    queryset = BoardType.objects.all()
    serializer_class = BoardTypeSerializer

