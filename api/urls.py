from django.urls import include, path

from .views import LoginAPI, LogoutAPI, BreachAPI, ResultAPI, BluetoothAPI

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='api-login'),
    path('logout/', LogoutAPI.as_view(), name='api-logout'),
    path('breach/', BreachAPI.as_view(), name='api-breach'),
    path('result/', ResultAPI.as_view(), name='api-result'),
    path('bluetooth/', BluetoothAPI.as_view(), name='api-bluetooth'),
]