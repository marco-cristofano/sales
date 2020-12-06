from rest_framework import serializers

from product.models import (
    Brand,
    Product,
    ProductsSales,
    Sale
)
from product.helpers import ProductBrand


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = (
            'name',
            'country',
            'address'
        )


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'description',
            'weight',
            'stock',
            'price',
            'brand'
        )


class BrandAndProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = (
            'description',
            'weight',
            'stock',
            'price',
            'brand'
        )


class ProductCountSalesSerializer(BrandAndProductSerializer):
    brand = BrandSerializer()
    total_sales = serializers.SerializerMethodField()

    def get_total_sales(self, instance):
        return instance.products_sales.count()

    class Meta:
        model = Product
        fields = (
            'description',
            'weight',
            'stock',
            'price',
            'brand',
            'total_sales'
        )


class SaleSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Sale
        fields = (
            'employee',
            'datetime',
            'products'
        )


class ProductsSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsSales
        fields = (
            'product',
            'sale',
            'price'
        )
        read_only_fields = ('price',)

    def create(self, validated_data):
        validated_data['price'] = validated_data['product'].price
        return super().create(validated_data)


class ProductsWithBrandSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    weight = serializers.DecimalField(max_digits=7, decimal_places=3)
    stock = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=13, decimal_places=3)
    brand_name = serializers.CharField(max_length=100)
    brand_country = serializers.CharField(max_length=100, required=False)
    brand_address = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return ProductBrand().create(validated_data)

    def update(self, product, validated_data):
        return ProductBrand().update(product, validated_data)
