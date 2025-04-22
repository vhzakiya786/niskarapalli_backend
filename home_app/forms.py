from django import forms
from .models import UserModel

class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = [
            'name', 'mobile', 'offer', 'offer_description', 'year',
            'upi_id1', 'upi_id2', 'upi_id3', 'upi_id4',
            'jan', 'feb', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ]
        widgets = {
            'offer': forms.CheckboxInput(),
            'jan': forms.NumberInput(attrs={'step': '0.01'}),
            'feb': forms.NumberInput(attrs={'step': '0.01'}),
            'march': forms.NumberInput(attrs={'step': '0.01'}),
            'april': forms.NumberInput(attrs={'step': '0.01'}),
            'may': forms.NumberInput(attrs={'step': '0.01'}),
            'june': forms.NumberInput(attrs={'step': '0.01'}),
            'july': forms.NumberInput(attrs={'step': '0.01'}),
            'august': forms.NumberInput(attrs={'step': '0.01'}),
            'september': forms.NumberInput(attrs={'step': '0.01'}),
            'october': forms.NumberInput(attrs={'step': '0.01'}),
            'november': forms.NumberInput(attrs={'step': '0.01'}),
            'december': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        mobile = cleaned_data.get('mobile')
        upi_id1 = cleaned_data.get('upi_id1')
        upi_id2 = cleaned_data.get('upi_id2')

        # If upi_id1 exists, check if it matches an existing user
        if upi_id1:
            existing_user = UserModel.objects.filter(upi_id1=upi_id1).first()
            if existing_user and upi_id2:
                # If upi_id1 matches, new UPI ID should go to upi_id2
                cleaned_data['upi_id2'] = upi_id2
                cleaned_data['upi_id1'] = existing_user.upi_id1
                cleaned_data['name'] = existing_user.name
                cleaned_data['mobile'] = existing_user.mobile

        return cleaned_data