# Generated by Django 4.0.4 on 2022-05-05 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fidia', '0004_user_privatekey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='privatekey',
            field=models.TextField(null=True),
        ),
    ]
