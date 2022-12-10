from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ("product", "quantity", "price")

    def validate_quantity(self, value):
        if value < 1:
            raise ValidationError("product quantity less than 1")
        return value


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = "__all__"

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for position in positions:
            stock.positions.create(**position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for position in positions:
            stock.positions.update_or_create(stock=stock, product=position['product'], defaults=position)
        return stock