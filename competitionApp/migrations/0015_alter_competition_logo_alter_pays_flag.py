# Generated by Django 4.1.7 on 2023-06-19 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitionApp', '0014_competition_identifiant_pays_abr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='logo',
            field=models.ImageField(blank=True, default='media/images/competitions/default.png', max_length=255, null=True, upload_to='static/images/competitions/'),
        ),
        migrations.AlterField(
            model_name='pays',
            name='flag',
            field=models.ImageField(blank=True, default='media/images/pays/default.png', max_length=255, null=True, upload_to='static/images/pays/'),
        ),
    ]
