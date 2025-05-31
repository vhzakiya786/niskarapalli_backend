from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Custom field to auto-update datetime on save
class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

# Abstract base model for common fields
class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class Member(BaseModel):
    name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100,blank=True,null=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,null=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be valid.")]
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Optional email address of the member."
    )

    def __str__(self):
        name=self.name
        if self.family_name:
            name=name+" "+self.family_name
        return name

    class Meta:
        db_table = "members"
        ordering = ['name']

class Donation(BaseModel):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('GOOGLE_PAY', 'Google Pay'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    )
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    donation_date = models.DateField()
    is_anonymous = models.BooleanField(default=False)
    purpose = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "donations"

    def __str__(self):
        return f"{'Anonymous' if self.is_anonymous else self.member.name if self.member else 'Unknown'} - {self.amount}"

class Subscription(BaseModel):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('GOOGLE_PAY', 'Google Pay'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    subscription_date = models.DateField()

    class Meta:
        db_table = "subscription"

    def __str__(self):
        return f"{self.member.name} - {self.amount} ({self.subscription_date})"

class ImamSalary(BaseModel):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('GOOGLE_PAY', 'Google Pay'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "imam_salary"

    def __str__(self):
        return f"Imam Salary - {self.amount} ({self.payment_date})"

class Expense(BaseModel):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('GOOGLE_PAY', 'Google Pay'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=100)
    expense_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "expenses"

    def __str__(self):
        return f"{self.purpose} - {self.amount} ({self.expense_date})"

class AuditLog(BaseModel):
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)

    class Meta:
        db_table = "audit_logs"

    def __str__(self):
        return f"{self.action} on {self.model_name} ({self.object_id}) at {self.timestamp}"