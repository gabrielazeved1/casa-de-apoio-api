from django.db import models
from .base import BaseModel
from .checkin import Checkin


class Checkout(BaseModel):
    class Meta:
        verbose_name_plural = "Check-out's"
        verbose_name = "Check-out"

    # um checkin para um checkout
    # se um checkin ja estiver um checkout nao pode apagar
    # problema-> quando relaciona um checkin com checkout, a coluna active continua com true
    # 2 melhoria - trocar true -> false
    checkin = models.OneToOneField(Checkin, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fechado em")

    def __str__(self):
        return self.checkin.person.name + " " + self.created_at.strftime("%d/%m/%Y")
