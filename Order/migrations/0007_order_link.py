# Generated by Django 3.2.13 on 2023-02-08 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0006_auto_20230201_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Link',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
