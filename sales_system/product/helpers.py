from product.models import (
    Brand,
    Product
)


class ProductBrand():

    def create(self, product_brand):
        brand = Brand.objects.get_or_create(
            name=product_brand['brand_name'],
            country=product_brand['brand_country'],
            address=product_brand['brand_address'],
        )
        product = Product.objects.create(
            description=product_brand['description'],
            weight=product_brand['weight'],
            stock=product_brand['stock'],
            price=product_brand['price'],
            brand=brand[0]
        )
        return product

    def update(self, product, product_brand):
        brand = Brand.objects.get_or_create(
            name=product_brand['brand_name'],
            country=product_brand['brand_country'],
            address=product_brand['brand_address'],
        )
        product.description = product_brand['description']
        product.weight = product_brand['weight']
        product.stock = product_brand['stock']
        product.price = product_brand['price']
        product.brand = brand[0]
        product.save()
        return product
