from django.db import models
from decimal import Decimal

class Constant(models.Model):
    # masalan ijara sozlamalari
    min_owner_rental_days = models.PositiveIntegerField(default=30)   # Owner bilan shartnoma eng kam muddat (kun)
    min_renter_rental_hours = models.PositiveIntegerField(default=1)  # Renter bilan ijaraning eng kam muddati (soat)

    late_fee_percent = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal("10.00")
    )  # kechikkan vaqt uchun foiz

    default_owner_share_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("80.00"))
    default_company_share_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("20.00"))

    # kelajakda yana maydon qo'shish mumkin
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Tizim sozlamalari"

    class Meta:
        verbose_name = "Tizim sozlamasi"
        verbose_name_plural = "Tizim sozlamalari"
