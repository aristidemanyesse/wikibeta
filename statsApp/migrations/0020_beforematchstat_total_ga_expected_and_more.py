# Generated by Django 4.1.7 on 2023-08-27 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0019_remove_beforematchstat_points_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='beforematchstat',
            name='total_ga_expected',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='total_gs_expected',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
