# Generated by Django 3.2.19 on 2023-10-03 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0017_auto_20230926_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentlines',
            name='LineStatus',
            field=models.CharField(blank=True, default='bost_Open', max_length=100),
        ),
    ]
