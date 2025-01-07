from django.urls import path
from . import views
from .views import register,Faresetting,BusListCreateView,BalanceView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    #path('', sensor_data_view, name="homepage"),
    path('register/', register, name="register"),
    path('api/balance/', BalanceView.as_view(), name='get_balance'),
    path('login/', views.login),
    path('fares/', Faresetting, name='fare_view'),
    path('fares/update/<str:route_id>/', views.update_fare_rate, name='update_fare_rate'),
    path('buses/', BusListCreateView.as_view(), name='bus-list-create'),
    path('buses/<str:id>/edit/', views.edit_bus, name='edit_bus'),
    path('buses/<str:id>/delete/', views.delete_bus, name='delete_bus'),
    
]