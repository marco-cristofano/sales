from django.contrib import admin

# Register your models here.
from product.models import (
    Brand,
    Product,
    Sale
)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Sale)
