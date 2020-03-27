# Generated by Django 3.0.3 on 2020-03-27 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_auto_20200327_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaserecord',
            name='data_collection',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='order_date',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='photo_counter_cabinet',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='photo_of_counter',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='photo_roof_access',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='power_of_attorney',
        ),
        migrations.RemoveField(
            model_name='purchaserecord',
            name='video_counter',
        ),
        migrations.AddField(
            model_name='customer',
            name='invoice_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='offer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
