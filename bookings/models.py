from django.db import models
from django.contrib.auth.models import User
from trains.models import Train
import random


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    journey_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    # 🎟️ PNR Field (Unique)
    pnr = models.CharField(max_length=10, unique=True, blank=True)

     # 💳 Payment Status
    payment_status = models.CharField(max_length=20, default="PENDING")  # PENDING or PAID

    # 🔁 Generate Unique PNR
    def generate_unique_pnr(self):
        while True:
            pnr = str(random.randint(1000000000, 9999999999))  # 10-digit number
            if not Booking.objects.filter(pnr=pnr).exists():
                return pnr

    # 💾 Save Method Override
    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_unique_pnr()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.train.name} ({self.pnr})"