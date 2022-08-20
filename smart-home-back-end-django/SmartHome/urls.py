from django.urls import path
from rest_framework.routers import DefaultRouter

from EventLog.views import EventViewset
from .views import (
	DashboardViewSet, ModuleViewSet, ClientsViewSet, GPIOPinConfigViewSet, BoardTypeViewSet, ModuleWithClientViewSet)


router = DefaultRouter()
router.register(r'event_log', EventViewset, basename='eventLog')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'sensors', ModuleViewSet, basename='sensors')
router.register(r'modules-detail', ModuleWithClientViewSet, basename='sensors')
router.register(r'board_type', BoardTypeViewSet, basename='sensors')
router.register(r'clients', ClientsViewSet, basename='clientssss')
router.register(r'gpio_config', GPIOPinConfigViewSet, basename='gpio_config')
# urlpatterns = router.urls

# urlpatterns = [
# 	path('eventLog/', EventViewset.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='eventLog'),
# 	path('dashboard/', DashboardViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='dashboard'),
# 	path('sensors/', SensorViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='sensors'),
# 	path('sensors/<int:id>/', SensorViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='sensors'),
# 	path('clients/', ClientsViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='clients'),
# 	path('clients/<int:id>/', ClientsViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='clients'),
# 	path('gpio_config/', GPIOPinConfigViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='gpio_config'),
# 	path('gpio_config/<int:id>/', GPIOPinConfigViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='gpio_config')
# 	#path('clients/', clients, name='clients')
# 	# path('api', TodoListApiView.as_view()),
# 	# path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
# ]