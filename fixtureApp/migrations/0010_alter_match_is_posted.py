# Generated by Django 4.1.7 on 2023-06-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixtureApp', '0009_match_is_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='is_posted',
            field=models.BooleanField(default=False),
        ),
    ]
