from rest_framework import (
    generics,
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.response import Response

from product.serializers import (
    BrandAndProductSerializer,
    BrandSerializer,
    ProductSerializer,
    ProductsSalesSerializer,
    ProductCountSalesSerializer,
    ProductsWithBrandSerializer,
    SaleSerializer
)
from product.models import (
    Brand,
    Product,
    Sale
)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def destroy(self, request, pk=None):
        brand = self.get_object()
        if not brand.products.exists():
            self.perform_destroy(brand)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            'exist related product', status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'], url_path='count_sales')
    def count_sales_retrieve(self, request, pk=None):
        employee = self.get_object()
        serializer = ProductCountSalesSerializer(employee)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='count_sales')
    def count_sales_list(self, request):
        employees = self.get_queryset()
        serializer = ProductCountSalesSerializer(employees, many=True)
        return Response(serializer.data)


class BrandAndProductViewSet(viewsets.ViewSetMixin, generics.ListAPIView):
    queryset = Product.objects.all().select_related('brand')
    serializer_class = BrandAndProductSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class ProductsSalesViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('brand')
    serializer_class = ProductsSalesSerializer


class ProductsWithBrandViewSet(viewsets.ViewSet, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsWithBrandSerializer

    def list(self, request):
        products = self.get_queryset()
        data = BrandAndProductSerializer(products, many=True).data
        return Response(data)

    def retrieve(self, request, pk=None):
        product = self.get_object()
        data = BrandAndProductSerializer(product).data
        return Response(data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        data = BrandAndProductSerializer(product).data
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        product = self.get_object()
        serializer = self.serializer_class(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        data = BrandAndProductSerializer(product).data
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
