from django.contrib import admin
from .models import Product, Order
# Register your models here.
import decimal
import csv


class QuestionAdminSite(admin.ModelAdmin):
    model = Product
    fields = ['product_name', 'product_descripton', 'category', 'price', 'amount_discount',
              'is_discount', 'publication_date']
    list_display = ('product_name', 'product_descripton', 'category', 'price', 'amount_discount',
                    'is_discount', 'publication_date'
                    )

    list_filter = ('price', 'publication_date')

    search_fields = ['product_name']


class OrderAdminSite(admin.ModelAdmin):
    model = Order
    fields = ['name', 'email', 'subject_marketing',
              'content_marketing']
    list_display = ('name', 'email', 'subject_marketing',
                    'content_marketing', 'created_at'
                    )

    list_filter = ('name', 'email')

    search_fields = ['email']


admin.site.register(Order, OrderAdminSite)
admin.site.register(Product, QuestionAdminSite)
