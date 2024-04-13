from django.db import models
from security.models import User, Image_extension_validator, picture_path


class Agency(models.Model):
    agent = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    registrationid = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class Photo(models.Model):
    img = models.ImageField(
        upload_to=picture_path,
        blank=True,
        validators=[Image_extension_validator]
    )


class Flight(models.Model):
    airline = models.CharField(max_length=100)
    agency = models.ForeignKey(
        Agency, on_delete=models.CASCADE, null=True, blank=True)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.ManyToManyField(Photo, blank=True)

    def __str__(self) -> str:
        return str(self.airline)


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    agency = models.ForeignKey(
        Agency, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.ManyToManyField(Photo, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Activity(models.Model):
    name = models.CharField(max_length=100)
    agency = models.ForeignKey(
        Agency, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.ManyToManyField(Photo, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class Package(models.Model):
    name = models.CharField(max_length=100)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hotels = models.ManyToManyField(Hotel, blank=True)
    flights = models.ManyToManyField(Flight, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class CustomPackage(models.Model):
    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='custom')
    flights = models.ManyToManyField(Flight, blank=True)
    hotels = models.ManyToManyField(Hotel, blank=True)
    activities = models.ManyToManyField(Activity, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return str(self.customer)


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, null=True, blank=True)
    custom = models.ForeignKey(
        CustomPackage, on_delete=models.CASCADE, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    payment_info = models.TextField(null=True, blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.customer)
    
    
class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.amount)
