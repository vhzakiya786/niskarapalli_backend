from django import forms
from .models import UserModel

class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'mobile', 'offer', 'offer_description', 'year',
                  'upi_id1', 'upi_id2', 'upi_id3', 'upi_id4',
                  'jan', 'feb', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november', 'december']
        widgets = {
            'jan': forms.TextInput(attrs={'class': 'form-control'}),
            'feb': forms.TextInput(attrs={'class': 'form-control'}),
            'march': forms.TextInput(attrs={'class': 'form-control'}),
            'april': forms.TextInput(attrs={'class': 'form-control'}),
            'may': forms.TextInput(attrs={'class': 'form-control'}),
            'june': forms.TextInput(attrs={'class': 'form-control'}),
            'july': forms.TextInput(attrs={'class': 'form-control'}),
            'august': forms.TextInput(attrs={'class': 'form-control'}),
            'september': forms.TextInput(attrs={'class': 'form-control'}),
            'october': forms.TextInput(attrs={'class': 'form-control'}),
            'november': forms.TextInput(attrs={'class': 'form-control'}),
            'december': forms.TextInput(attrs={'class': 'form-control'}),
        }
