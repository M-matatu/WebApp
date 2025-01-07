from django.db import models
from django.contrib.auth.models import User

class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Lat: {self.latitude}, Long: {self.longitude}"

class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - KSh {self.balance}"

class coordinatesArd(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lat: {self.latitude}, Long: {self.longitude}"
    
class Fare(models.Model):
    route_id = models.CharField()
    route_start = models.CharField()
    route_end = models.CharField()
    Rate = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lat: {self.Route}, Long: {self.Rate}"
    
class Bus(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    id = models.CharField(max_length=10, unique=True, primary_key=True)
    routeStart = models.CharField(max_length=100)
    routeEnd = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    capacity = models.PositiveIntegerField()
    passengerCount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Bus {self.id} - {self.route_start} to {self.route_end}"