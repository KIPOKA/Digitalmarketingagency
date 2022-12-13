from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_descripton = models.CharField(max_length=150, default="")
    category = models.CharField(max_length=100, default="")
    subcategory = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)

    publication_date = models.DateField()

    def __str__(self):
        return self.product_name
