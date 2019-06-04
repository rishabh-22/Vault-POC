from django import forms
from .models import ContactQuery


class ContactQueryForm(forms.ModelForm):

    class Meta:
        model = ContactQuery
        fields = ('name', 'email', 'subject', 'query',)
