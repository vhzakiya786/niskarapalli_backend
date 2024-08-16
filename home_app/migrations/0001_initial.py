# Generated by Django 5.1 on 2024-08-11 07:41

import django.utils.timezone
import home_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', home_app.models.AutoDateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'expenses_model',
            },
        ),
        migrations.CreateModel(
            name='ReportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', home_app.models.AutoDateTimeField(default=django.utils.timezone.now)),
                ('month', models.CharField(max_length=25)),
                ('expense', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'reports_model',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', home_app.models.AutoDateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('offer', models.BooleanField(default=False)),
                ('offer_description', models.CharField(blank=True, max_length=255, null=True)),
                ('year', models.CharField(blank=True, max_length=10, null=True)),
                ('upi_id1', models.CharField(blank=True, max_length=255, null=True)),
                ('upi_id2', models.CharField(blank=True, max_length=255, null=True)),
                ('upi_id3', models.CharField(blank=True, max_length=255, null=True)),
                ('upi_id4', models.CharField(blank=True, max_length=255, null=True)),
                ('jan', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('feb', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('march', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('april', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('may', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('june', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('july', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('august', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('september', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('october', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('november', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('december', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
            options={
                'db_table': 'users_model',
            },
        ),
    ]
