# Generated by Django 4.1.4 on 2023-01-21 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competitionApp', '0007_alter_ligneranking_ranking_alter_ligneranking_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='ligneranking',
            name='ppg',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
