from django import forms
from .models import ContactQuery, UserAddress


class ContactQueryForm(forms.ModelForm):

    class Meta:
        model = ContactQuery
        fields = ('name', 'email', 'subject', 'query',)


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = ('label', 'address', 'landmark', 'city', 'state', 'country', 'pincode', 'mobile')
