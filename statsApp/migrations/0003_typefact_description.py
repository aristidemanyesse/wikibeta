# Generated by Django 4.1.4 on 2022-12-25 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0002_typefact_fact'),
    ]

    operations = [
        migrations.AddField(
            model_name='typefact',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
