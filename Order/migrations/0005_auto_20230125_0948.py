# Generated by Django 3.2.13 on 2023-01-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0004_auto_20230120_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='U_LAT',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='U_LONG',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
