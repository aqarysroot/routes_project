from django import forms

from cities.models import City


class HtmlForm(forms.Form):
    name = forms.CharField(label='City')


class CityForm(forms.ModelForm):
    name = forms.CharField(label='Create City', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the name of city'
    }))

    class Meta:
        model = City
        fields = ('name', )