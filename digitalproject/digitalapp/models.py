from django.db import models


# Create your models here.


class Product(models.Model):

    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_description = models.CharField(max_length=150, default="")
    category = models.CharField(max_length=100, default="")
    subcategory = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    amount_discount = models.IntegerField(default=0)
    is_discount = models.BooleanField(default=False)
    created_at = models.DateField()

    def discount(self):
        amount_discount = 0
        if self.is_discout == True:
            amount_discount = self.price - (self.price * self.amount_discount)
            return amount_discount

    def __str__(self):
        return self.product_name


class Order(models.Model):
    user = None
    name = models.CharField(max_length=90)
    subject_marketing = models.CharField(max_length=200, default="")
    content_marketing = models.TextField(max_length=200, default="")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
