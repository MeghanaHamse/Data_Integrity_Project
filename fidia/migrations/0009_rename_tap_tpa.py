# Generated by Django 4.0.4 on 2022-05-05 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fidia', '0008_alter_auditrequest_cloudauditat_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TAP',
            new_name='TPA',
        ),
    ]