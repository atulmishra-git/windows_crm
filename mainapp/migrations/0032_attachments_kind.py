# Generated by Django 3.0.3 on 2020-05-01 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0031_attachmenttemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachments',
            name='kind',
            field=models.CharField(default='custom', max_length=16, verbose_name='kind'),
        ),
    ]