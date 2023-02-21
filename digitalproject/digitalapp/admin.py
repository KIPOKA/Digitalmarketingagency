from django.contrib import admin
from .models import Product, Order
# Register your models here.


class ProductAdminSite(admin.ModelAdmin):
    model = Product

    fields = ['product_name', 'product_descripton', 'category', 'price', 'amount_discount',
              'is_discount', 'created_at']
    list_display = ('product_name', 'product_descripton', 'category', 'price', 'amount_discount',
                    'is_discount', 'created_at'
                    )

    list_filter = ('price', 'created_at')

    search_fields = ['product_name']


class OrderAdminSite(admin.ModelAdmin):
    model = Order
    fields = ['name', 'subject_marketing',
              'content_marketing']
    list_display = ('name',  'subject_marketing',
                    'content_marketing', 'created_at'
                    )

    list_filter = ('name', 'created_at')
    search_fields = ['name']


admin.site.register(Order, OrderAdminSite)
admin.site.register(Product, ProductAdminSite)
