# Generated by Django 4.0.4 on 2022-05-04 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fidia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='biometricimage',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
