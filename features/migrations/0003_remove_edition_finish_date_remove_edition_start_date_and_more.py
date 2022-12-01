# Generated by Django 4.1.3 on 2022-12-01 12:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0002_alter_edition_finish_date_alter_edition_start_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edition',
            name='finish_date',
        ),
        migrations.RemoveField(
            model_name='edition',
            name='start_date',
        ),
        migrations.AddField(
            model_name='editioncompetition',
            name='finish_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='editioncompetition',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='BeforeMatchStat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('home_ppg', models.IntegerField(blank=True, null=True)),
                ('away_ppg', models.IntegerField(blank=True, null=True)),
                ('home_avg_scored', models.IntegerField(blank=True, null=True)),
                ('home_avg_conceded', models.IntegerField(blank=True, null=True)),
                ('away_avg_scored', models.IntegerField(blank=True, null=True)),
                ('away_avg_conceded', models.IntegerField(blank=True, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='before_stat_match', to='features.match')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
