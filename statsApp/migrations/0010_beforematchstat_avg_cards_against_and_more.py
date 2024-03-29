# Generated by Django 4.1.4 on 2023-01-18 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fixtureApp', '0005_remove_match_referer_delete_referer'),
        ('statsApp', '0009_rename_only_precision_fact_all_matches'),
    ]

    operations = [
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_cards_against',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_cards_for',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_corners_against',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_corners_for',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_fouls_against',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_fouls_for',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_offside_against',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_offside_for',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_shots_against',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_shots_for',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_shots_target_against',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='avg_shots_target_for',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='extrainfosmatch',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_info_match', to='fixtureApp.match'),
        ),
    ]
