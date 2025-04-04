# Generated by Django 5.1.3 on 2025-03-11 13:51

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(blank=True, null=True, verbose_name='Updated at')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Address')),
                ('company_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Company Name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone Number')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('type_vacation', models.CharField(blank=True, choices=[('FULL', 'Full Time'), ('PART', 'Part Time'), ('REMOTE', 'Remote Time')], max_length=20, null=True, verbose_name='Type Vacation')),
                ('requirements', models.TextField(blank=True, null=True, verbose_name='Requirements')),
                ('responsibilities', models.TextField(blank=True, null=True, verbose_name='Responsibilities')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Updated by')),
            ],
            options={
                'verbose_name': 'Vacation',
                'verbose_name_plural': 'Vacations',
            },
        ),
    ]
