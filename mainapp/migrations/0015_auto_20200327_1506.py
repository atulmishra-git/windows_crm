# Generated by Django 3.0.3 on 2020-03-27 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20200327_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaserecord',
            name='kwp',
        ),
        migrations.AlterField(
            model_name='purchaserecord',
            name='module_count',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='purchaserecord',
            name='watt',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]