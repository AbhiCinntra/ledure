# Generated by Django 3.2.19 on 2023-08-02 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JournalEntries', '0002_auto_20230711_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentries',
            name='U_Cancel',
            field=models.CharField(blank=True, default='N', max_length=200),
        ),
    ]
