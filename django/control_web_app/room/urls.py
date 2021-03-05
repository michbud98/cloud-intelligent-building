from django.urls import path

from .views import room_list_view, room_create_view, room_detail_view, room_remove_view, room_update_view

urlpatterns = [
    # root path for this django app is [rooms]
    path('', room_list_view, name='room_list'),
    path('room_create', room_create_view, name='room_create'),
    path('<int:room_id>', room_detail_view, name='room_detail'),
    path('<int:room_id>/update', room_update_view, name='room_update'),
    path('<int:room_id>/remove', room_remove_view, name='room_remove'),

]
