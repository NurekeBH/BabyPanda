from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Product, VipClient
from .serializers import ProductSerializer, VipClientSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VipClient
import phonenumbers
from phonenumbers import NumberParseException


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class VipClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VipClient.objects.all()
    serializer_class = VipClientSerializer
    lookup_field = "phone_number"


@api_view(["GET"])
def check_phone(request):
    raw_phone = request.GET.get("phone")

    if not raw_phone:
        return Response({"error": "Phone required"}, status=400)

    try:
        # Қазақстандық нөмір ретінде парсинг
        parsed = phonenumbers.parse(raw_phone, "KZ")
        # Халықаралық форматқа келтіру (мысалы: +77474115049)
        normalized_phone = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.E164
        )
    except NumberParseException:
        return Response({"error": "Invalid phone format"}, status=400)

    # Базадан нақты сол форматпен іздеу
    exists = VipClient.objects.filter(phone_number=normalized_phone).exists()
    return Response({"exists": exists})
