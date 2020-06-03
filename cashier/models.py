from django.db import models


# Create your models here.
class Cashier(models.Model):
    cashier_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, primary_key=True)
    merchant = models.CharField(max_length=50)
    merchant_branch = models.CharField(max_length=50)
    cashier_password = models.CharField(max_length=60)

    class Meta:
        db_table = "cashier"

    def __str__(self):
        return self.username
