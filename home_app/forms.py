from django import forms
from .models import Member, Donation, Subscription, ImamSalary, Expense
from django.core.validators import RegexValidator

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'phone_number', 'email','family_name']
        widgets = {
            'name': forms.TextInput(attrs={ "class":"border p-2 rounded w-full autocomplete-name"}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+1234567890'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['member', 'amount', 'payment_method', 'transaction_id', 'upi_id', 'donation_date', 'is_anonymous', 'purpose']
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date'}),
            'member': forms.Select(attrs={'class': 'autocomplete'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Transaction ID (optional)'}),
            'upi_id': forms.TextInput(attrs={'placeholder': 'UPI ID (optional)'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_anonymous') and cleaned_data.get('member'):
            raise forms.ValidationError("Anonymous donations cannot have a member associated.")
        return cleaned_data

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['member', 'amount', 'payment_method', 'transaction_id', 'upi_id', 'subscription_date']
        widgets = {
            'subscription_date': forms.DateInput(attrs={'type': 'date'}),
            'member': forms.Select(attrs={'class': 'autocomplete'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Transaction ID (optional)'}),
            'upi_id': forms.TextInput(attrs={'placeholder': 'UPI ID (optional)'}),
        }

class ImamSalaryForm(forms.ModelForm):
    class Meta:
        model = ImamSalary
        fields = ['amount', 'payment_date', 'payment_method', 'transaction_id', 'upi_id', 'notes']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Transaction ID (optional)'}),
            'upi_id': forms.TextInput(attrs={'placeholder': 'UPI ID (optional)'}),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'purpose', 'expense_date', 'payment_method', 'transaction_id', 'upi_id', 'notes']
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Transaction ID (optional)'}),
            'upi_id': forms.TextInput(attrs={'placeholder': 'UPI ID (optional)'}),
        }