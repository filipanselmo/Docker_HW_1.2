from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello')


class StockSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)

        param = request.query_params.get('products')
        if not param:
            return queryset

        if param.isnumeric():
            return queryset.filter(Q(products__id__in=[param]))

        products = Product.objects.filter(Q(title__contains=param) | Q(description__contains=param))
        products_pk = [p.id for p in products]
        return queryset.filter(Q(products__id__in=products_pk))


class ProductSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)

        param = request.query_params.get('search')
        if not param:
            return queryset

        return queryset.filter(Q(title__contains=param) | Q(description__contains=param))


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [ProductSearchFilter]
    pagination_class = PageNumberPagination


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [StockSearchFilter]
    pagination_class = PageNumberPagination