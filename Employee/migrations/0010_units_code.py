# Generated by Django 4.0.3 on 2023-02-28 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0009_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='Code',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
