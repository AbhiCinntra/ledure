# Generated by Django 3.2.13 on 2023-03-08 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0015_auto_20230308_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentlines',
            name='UnitPriceown',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
    ]
