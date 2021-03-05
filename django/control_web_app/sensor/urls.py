from django.urls import path

from .views import (sensor_list_view, sensor_create_view,
 sensor_remove_view, sensor_detail_view, sensor_update_view)

urlpatterns = [
    # root path for this django app is [sensors]
    path('', sensor_list_view, name='sensor_list'),
    path('<str:sensor_id>', sensor_detail_view, name='sensor_detail'),
    path('<str:sensor_id>/<str:hostname>/<str:sensor_type>/create', sensor_create_view, name='sensor_create'),
    path('<str:sensor_id>/update', sensor_update_view, name='sensor_update'),
    path('<str:sensor_id>/remove', sensor_remove_view, name='sensor_remove'),
]