# Generated by Django 4.1.3 on 2022-11-26 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('betting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oddsmatch',
            name='away',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AlterField(
            model_name='oddsmatch',
            name='draw',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
        migrations.AlterField(
            model_name='oddsmatch',
            name='home',
            field=models.FloatField(blank=True, default=1.0, null=True),
        ),
    ]