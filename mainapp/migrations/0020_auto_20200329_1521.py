# Generated by Django 3.0.3 on 2020-03-29 15:21

from django.db import migrations
import mainapp.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_callnotes_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attachments',
            old_name='file_type',
            new_name='file_name',
        ),
        migrations.RemoveField(
            model_name='attachments',
            name='file_link',
        ),
        migrations.AlterField(
            model_name='attachments',
            name='upload',
            field=mainapp.fields.ContentTypeRestrictedFileField(null=True, upload_to='uploads/'),
        ),
    ]