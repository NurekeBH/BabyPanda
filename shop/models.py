from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import os
import uuid


def product_image_upload_path(instance, filename):
    """
    Генерирует уникальное имя файла для сохранения в MEDIA_ROOT/product_images/.
    Сохраняет оригинальное расширение.
    """
    # Берём расширение из исходного имени
    ext = filename.split(".")[-1].lower()
    # Генерируем уникальный идентификатор
    unique_name = uuid.uuid4().hex
    # Собираем новое имя
    new_filename = f"{unique_name}.{ext}"
    # Опционально можно разбивать по подпапкам:
    # return os.path.join('product_images', unique_name[:2], new_filename)
    return os.path.join("product_images", new_filename)


class VipClient(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(
        region="KZ", unique=True, verbose_name="Телефон нөмірі"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Child(models.Model):
    GENDER_CHOICES = [
        ("M", "Ұл"),
        ("F", "Қыз"),
    ]
    vip_client = models.ForeignKey(
        VipClient, related_name="children", on_delete=models.CASCADE
    )
    child_full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, verbose_name="Жыныс"
    )

    def __str__(self):
        return self.child_full_name


class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    wholesale_price = models.DecimalField(
        "Цена оптом", max_digits=10, decimal_places=0, default=0
    )
    retail_price = models.DecimalField(
        "Цена розница", max_digits=10, decimal_places=0, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to=product_image_upload_path,
        null=True,  # позволяет базе хранить NULL
        blank=True,  # позволяет форме оставлять поле пустым
    )

    def __str__(self):
        return f"Image for {self.product.name}"


class Order(models.Model):
    vip_client = models.ForeignKey(
        VipClient, related_name="orders", on_delete=models.CASCADE
    )
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} for {self.vip_client.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
