# Generated by Django 4.1.7 on 2023-07-02 20:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teamApp', '0004_remove_team_is_club_alter_team_logo'),
        ('fixtureApp', '0010_alter_match_is_posted'),
        ('statsApp', '0014_alter_resultmatch_away_half_score_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamProfileMatch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('dynamic', models.FloatField(blank=True, default=0.0, null=True)),
                ('attack', models.FloatField(blank=True, default=0.0, null=True)),
                ('defense', models.FloatField(blank=True, default=0.0, null=True)),
                ('pression', models.FloatField(blank=True, default=0.0, null=True)),
                ('clean', models.FloatField(blank=True, default=0.0, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_profile', to='fixtureApp.match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_profile', to='teamApp.editionteam')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
