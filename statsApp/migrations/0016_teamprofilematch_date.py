# Generated by Django 4.1.7 on 2023-07-02 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0015_teamprofilematch'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamprofilematch',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
