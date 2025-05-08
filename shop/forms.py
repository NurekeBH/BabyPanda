# shop/forms.py
from django import forms
from .models import VipClient


class VipClientForm(forms.ModelForm):
    class Meta:
        model = VipClient
        fields = "__all__"
        widgets = {
            "phone_number": forms.TextInput(attrs={"placeholder": "+7(___)___ __ __"}),
        }

    class Media:
        # 1) Mask плагині, 2) біздің phone_mask.js
        js = [
            "https://cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js",
            "shop/js/phone_mask.js",
        ]
