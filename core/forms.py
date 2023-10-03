from django import forms
from core.models import DnsReclamation


class DomaineForm(forms.ModelForm):

    class Meta:
        model = DnsReclamation
        fields = '__all__'
        exclude = ('slug', 'traiter', )
