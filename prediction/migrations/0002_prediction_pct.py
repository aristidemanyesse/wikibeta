# Generated by Django 4.1.3 on 2022-12-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='pct',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
