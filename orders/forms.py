from django import forms
from .models import Order
from localflavor.us.forms import USZipCodeField


class OrderCreateForm(forms.ModelForm):
    # valid United States
    # zip code is required to create a new order
    # instead of normal form
    # you need to type zip code as US conditions
    postal_code = USZipCodeField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']
