from django.db import models

# Create your models here.
class calculation_database(models.Model):
    # Amount field
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Percentage field
    percentage = models.DecimalField(max_digits=4, decimal_places=2)

    # Years field
    years = models.IntegerField()

    # Monthly Payment field
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)

    # total Payment field
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)