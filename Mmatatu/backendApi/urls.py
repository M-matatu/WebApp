from django.urls import path
from .views import passapi, driverapi,gsmcoords

urlpatterns = [
    
    path('passenger/', passapi.as_view(), name="location"),
    path('driver/', driverapi.as_view(), name="images"),
    path('arduinoCoords/', gsmcoords.as_view(), name="images"),   
]