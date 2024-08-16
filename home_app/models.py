from django.db import models

# Create your models here.
from django.utils import timezone


from home_app.helpers import fn_update_google_sheet

class AutoDateTimeField(models.DateTimeField):
	def pre_save(self, model_instance, add):
		return timezone.now()
class BaseModel(models.Model):
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = AutoDateTimeField(default=timezone.now)

	class Meta:
		abstract = True
		

class UserModel(BaseModel):
	name = models.CharField(max_length=255,blank=True, null=True)
	mobile = models.CharField(max_length=20,blank=True, null=True)
	offer = models.BooleanField(default=False)
	offer_description=models.CharField(max_length=255,blank=True, null=True)
	year = models.CharField(max_length=10,blank=True, null=True)
	upi_id1 = models.CharField(max_length=255, blank=True, null=True)
	upi_id2 = models.CharField(max_length=255, blank=True, null=True)
	upi_id3 = models.CharField(max_length=255, blank=True, null=True)
	upi_id4 = models.CharField(max_length=255, blank=True, null=True)
	jan = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	feb = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	march = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	april = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	may = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	june = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	july = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	august = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	september = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	october = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	november = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	december = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		db_table ="users_model"

	def __str__(self):
		return self.name


class ExpenseModel(BaseModel):
	name=models.CharField(max_length=255)
	amount=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		db_table ="expenses_model"

	def __str__(self):
		return self.name
	
class ReportModel(BaseModel):
	month=models.CharField(max_length=25)
	expense=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	balance=models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		db_table ="reports_model"

	def __str__(self):
		return self.month






