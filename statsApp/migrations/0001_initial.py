# Generated by Django 4.1.4 on 2022-12-13 21:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teamApp', '0001_initial'),
        ('fixtureApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultMatch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('home_score', models.IntegerField(blank=True, default=0, null=True)),
                ('away_score', models.IntegerField(blank=True, default=0, null=True)),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
                ('home_half_score', models.IntegerField(blank=True, default=0, null=True)),
                ('away_half_score', models.IntegerField(blank=True, default=0, null=True)),
                ('result_half', models.CharField(blank=True, max_length=255, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_match', to='fixtureApp.match')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExtraInfosMatch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('home_shots', models.IntegerField(blank=True, default=0, null=True)),
                ('away_shots', models.IntegerField(blank=True, default=0, null=True)),
                ('home_shots_on_target', models.IntegerField(blank=True, default=0, null=True)),
                ('away_shots_on_target', models.IntegerField(blank=True, default=0, null=True)),
                ('home_corners', models.IntegerField(blank=True, default=0, null=True)),
                ('away_corners', models.IntegerField(blank=True, default=0, null=True)),
                ('home_fouls', models.IntegerField(blank=True, default=0, null=True)),
                ('away_fouls', models.IntegerField(blank=True, default=0, null=True)),
                ('home_offsides', models.IntegerField(blank=True, default=0, null=True)),
                ('away_offsides', models.IntegerField(blank=True, default=0, null=True)),
                ('home_yellow_cards', models.IntegerField(blank=True, default=0, null=True)),
                ('away_yellow_cards', models.IntegerField(blank=True, default=0, null=True)),
                ('home_red_cards', models.IntegerField(blank=True, default=0, null=True)),
                ('away_red_cards', models.IntegerField(blank=True, default=0, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_match', to='fixtureApp.match')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BeforeMatchStat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('ppg', models.FloatField(blank=True, null=True)),
                ('goals_scored', models.FloatField(blank=True, null=True)),
                ('avg_goals_scored', models.FloatField(blank=True, null=True)),
                ('goals_conceded', models.FloatField(blank=True, null=True)),
                ('avg_goals_conceded', models.FloatField(blank=True, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='before_stat_match', to='fixtureApp.match')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_stat_match', to='teamApp.editionteam')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
