from rest_framework import routers

from employee.api import (
    EmployeeViewSet,
    TelephoneViewSet
)

from product.api import (
    BrandAndProductViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductsSalesViewSet,
    ProductsWithBrandViewSet,
    SaleViewSet
)


router = routers.DefaultRouter()
router.register(r'employee', EmployeeViewSet)
router.register(r'telephone', TelephoneViewSet)
router.register(r'brand', BrandViewSet)
router.register(r'product', ProductViewSet)
router.register(r'products_sales', ProductsSalesViewSet)
router.register(r'products_with_brand', ProductsWithBrandViewSet)
router.register(r'brand_and_product', BrandAndProductViewSet)
router.register(r'sale', SaleViewSet)
urlpatterns = router.urls
