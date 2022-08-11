from django import forms
from django.utils.translation import gettext_lazy as _

# tuple (count, value)
# coerce: for convert the value to integer
PRODUCT_QUANTITY_CHOICES = ((i, str(i)) for i in range(1, 21))


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int,  # for convert the input to integer
                                      label=_('Quantity'))
    # hidden input fill it by views default false
    override = forms.BooleanField(required=False, initial=False,
                                  widget=forms.HiddenInput)
