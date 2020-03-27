# Generated by Django 3.0.3 on 2020-03-27 09:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20200327_0812'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaserecord',
            name='ac_date',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='offer_created',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='price_with_tax',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='send_by_email',
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='ac_mechanic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='ac_term',
            field=models.DateField(blank=True, null=True, verbose_name='AC Termin'),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='alignment',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='date_sent',
            field=models.DateField(null=True, verbose_name='AG geschickt/AG Sent'),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='dc_mechanic',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='dc_term',
            field=models.DateField(blank=True, null=True, verbose_name='DC Termin'),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='declined',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='manufacturer',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='module_area',
            field=models.FloatField(help_text='Area in meter squared (m2)', null=True, validators=[django.core.validators.MinValueValidator(0, 'Should be above 0')]),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='offer_by',
            field=models.CharField(choices=[('Email', 'Via Email'), ('Letter', 'Via Letter')], max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='offer_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='roof_tilt',
            field=models.FloatField(help_text='in Degrees', null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='roof_type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='purchaserecord',
            name='watt',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='purchaserecord',
            name='price_without_tax',
            field=models.FloatField(help_text='Price in Euro (€)', null=True, validators=[django.core.validators.MinValueValidator(0, 'Should be above 0')]),
        ),
        migrations.AlterField(
            model_name='purchaserecord',
            name='project_planning_created',
            field=models.BooleanField(blank=True, default=True, verbose_name='Projektierung Erstellt'),
        ),
        migrations.AlterField(
            model_name='purchaserecord',
            name='reseller_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='purchaserecord',
            name='with_battery',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
