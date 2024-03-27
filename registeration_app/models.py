from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=100)

class Agent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=100)

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Flight(models.Model):
    name = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.source} to {self.destination}"

class View(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class TravelPackage(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class PackageItem(models.Model):
    PACKAGE_TYPES = (
        ('default', 'Default'),
        ('custom', 'Custom'),
    )

    package = models.ForeignKey(TravelPackage, related_name='items', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, null=True, blank=True, on_delete=models.CASCADE)
    view = models.ForeignKey(View, null=True, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=PACKAGE_TYPES)

    def __str__(self):
        return f"{self.package.name} - {self.get_type_display()}"

    @property
    def total_price(self):
        price = 0
        if self.hotel:
            price += self.hotel.price
        if self.flight:
            price += self.flight.price
        return price
