from django.contrib import admin
from .models import VipClient, Child, Product, ProductImage, Order, OrderItem
from .forms import VipClientForm


class ChildInline(admin.TabularInline):
    model = Child
    extra = 1
    fields = ("child_full_name", "birth_date", "gender")
    radio_fields = {"gender": admin.HORIZONTAL}


class VipClientAdmin(admin.ModelAdmin):
    form = VipClientForm
    list_display = ("full_name", "phone_number", "created_at")
    inlines = [ChildInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "product_code",
        "wholesale_price",
        "retail_price",
        "created_at",
    )
    inlines = [ProductImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "vip_client", "order_date", "total_amount")
    inlines = [OrderItemInline]


admin.site.register(VipClient, VipClientAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
