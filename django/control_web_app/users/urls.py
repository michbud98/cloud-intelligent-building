from django.urls import path

from django.urls import path, include

app_name = 'users'
urlpatterns = [
    # root path for this django app is [devices]
    path('', include('django.contrib.auth.urls')),
]