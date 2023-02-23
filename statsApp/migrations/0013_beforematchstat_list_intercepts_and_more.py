# Generated by Django 4.1.4 on 2023-02-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0012_alter_beforematchstat_list_confrontations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='beforematchstat',
            name='list_intercepts',
            field=models.TextField(blank=True, default='[]', null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='nb_cards_gt_avg_fouls',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='nb_corners_gt_avg_fouls',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='nb_matchs_gt_avg_fouls',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='nb_offside_gt_avg_fouls',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='nb_shots_gt_avg_fouls',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='nb_shots_target_gt_avg_fouls',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='beforematchstat',
            name='points',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
