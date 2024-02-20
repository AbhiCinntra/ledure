# Generated by Django 3.2.13 on 2022-07-18 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Campaign', '0002_auto_20220718_0944'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignSetMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=100)),
                ('Phone', models.CharField(blank=True, max_length=100)),
                ('Email', models.CharField(blank=True, max_length=100)),
                ('CampSetId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Campaign.campaignset')),
            ],
        ),
    ]
