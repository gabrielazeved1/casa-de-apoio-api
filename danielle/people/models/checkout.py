from django.db import models
from .base import BaseModel
from .checkin import Checkin


class Checkout(BaseModel):
    class Meta:
        verbose_name_plural = "Check-out's"
        verbose_name = "Check-out"

    # one checkin for one checkout
    # if a checkin already has a checkout, it cannot be deleted
    # problem -> when linking a checkin with a checkout, the active column remains true
    checkin = models.OneToOneField(Checkin, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fechado em")

    def __str__(self):
        return self.checkin.person.name + " " + self.created_at.strftime("%d/%m/%Y")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # improvement 2: change from true to false in active after checkout
        if self.checkin.active:
            self.checkin.active = False
            self.checkin.save()
