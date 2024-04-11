from django.db import models
from security.models import User


class Package(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Flight(models.Model):
    package = models.ForeignKey(
        Package, related_name='flights', on_delete=models.CASCADE)
    airline = models.CharField(max_length=100)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Hotel(models.Model):
    package = models.ForeignKey(
        Package, related_name='hotels', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)


class Activity(models.Model):
    package = models.ForeignKey(
        Package, related_name='activities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Booking(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    payment_info = models.TextField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)


class CustomPackage(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    flights = models.ManyToManyField(Flight)
    hotels = models.ManyToManyField(Hotel)
    activities = models.ManyToManyField(Activity)


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
