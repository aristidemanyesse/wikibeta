# Generated by Django 4.1.4 on 2023-01-07 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='editionteam',
            options={'ordering': ['team']},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='team',
            name='logo',
            field=models.ImageField(blank=True, default='', max_length=255, null=True, upload_to='static/images/teams/'),
        ),
    ]
