# Generated by Django 4.1.7 on 2023-06-21 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixtureApp', '0008_match_is_compared'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='is_posted',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
