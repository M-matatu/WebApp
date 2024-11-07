from django.urls import path
from .views import passapi, driverapi

urlpatterns = [
    #path('', backendapires.as_view(), name="homepage"),
    path('passenger/', passapi.as_view(), name="location"),
    path('driver/', driverapi.as_view(), name="images"),
   
]