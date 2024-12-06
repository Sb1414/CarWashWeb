from django.contrib.auth.models import User
from django.db import models

class Specialist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='specialists/', default='specialists/default_specialist.png')

    def __str__(self):
        return self.name

class Service(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='services', default=1)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/', default='services/default_service.png')
    duration = models.CharField(max_length=50, default='1 час')

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city}, {self.address}"


class Slot(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='slots')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='slots', null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    camera_active = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[
        ('Свободен', 'Свободен'),
        ('Забронирован', 'Забронирован'),
        ('Завершен', 'Завершен'),
    ], default='Свободен')

    def __str__(self):
        return f"{self.date} {self.time} ({self.get_status_display()})"


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Заказ {self.service.name} от {self.user.username}"

