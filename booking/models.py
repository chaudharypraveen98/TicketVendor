import uuid

from django.db import models


class Seat(models.Model):
    SEATNUM = models.CharField(max_length=8)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.SEATNUM} {str(self.status)}"


class Orders(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='ticket_orders', null=True, blank=True)
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    person_name = models.CharField(max_length=30)

    def __str__(self):
        return self.person_name
