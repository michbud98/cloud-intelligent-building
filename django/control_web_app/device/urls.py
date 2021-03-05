from django.urls import path

from .views import (device_list_view, device_create_view, device_update_view,
 device_detail_view, device_values_edit_view, device_value_get, device_remove_view)

urlpatterns = [
    # root path for this django app is [devices]
    path('', device_list_view, name='device_list'),
    path('device_create', device_create_view, name='device_create'),
    path('<str:device_id>', device_detail_view, name='device_detail'),
    path('<str:device_id>/<int:room_id>/edit_values', device_values_edit_view, name='device_values_edit'),
    path('<str:device_id>/get_value', device_value_get, name='device_values_edit'),
    path('<str:device_id>/update', device_update_view, name='device_update'),
    path('<str:device_id>/remove', device_remove_view, name='device_remove'),
]