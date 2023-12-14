# Generated by Django 4.1 on 2023-12-02 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0023_rename_clean_teamprofilematch_domination_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teamprofilematch',
            old_name='dynamic',
            new_name='dynamique',
        ),
        migrations.AddField(
            model_name='teamprofilematch',
            name='maitrise',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]