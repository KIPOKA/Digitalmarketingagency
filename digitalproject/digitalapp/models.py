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


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    company_name = models.CharField(max_length=150)
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=90)
    oid = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    payment_paid = models.CharField(max_length=20, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
