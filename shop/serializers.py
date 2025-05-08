from rest_framework import serializers
from .models import Product, ProductImage, VipClient, Child, Order, OrderItem


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "product_code",
            "name",
            "description",
            "wholesale_price",
            "retail_price",
            "images",
        ]


class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields = ["id", "child_full_name", "birth_date", "gender"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_date", "total_amount", "order_items"]


class VipClientSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = VipClient
        fields = ["id", "full_name", "phone_number", "children", "orders"]
