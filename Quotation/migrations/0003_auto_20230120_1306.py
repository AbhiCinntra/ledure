# Generated by Django 3.2.13 on 2023-01-20 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quotation', '0002_auto_20230117_1050'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quotation',
            old_name='additionalCharges',
            new_name='AdditionalCharges',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='deliveryMode',
            new_name='DeliveryCharge',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='deliveryTerm',
            new_name='DeliveryMode',
        ),
        migrations.RenameField(
            model_name='quotation',
            old_name='paymentType',
            new_name='DeliveryTerm',
        ),
        migrations.AddField(
            model_name='quotation',
            name='PaymentType',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='quotation',
            name='TermCondition',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='quotation',
            name='Unit',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
