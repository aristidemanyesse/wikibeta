# Generated by Django 4.1.4 on 2022-12-13 21:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teamApp', '0001_initial'),
        ('competitionApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('hour', models.TimeField(blank=True, null=True)),
                ('is_finished', models.BooleanField(blank=True, default=False, null=True)),
                ('away', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_match', to='teamApp.editionteam')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edition_du_match', to='competitionApp.editioncompetition')),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_match', to='teamApp.editionteam')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('minute', models.CharField(blank=True, max_length=255, null=True)),
                ('is_penalty', models.BooleanField(blank=True, default=False, null=True)),
                ('home_half_score', models.IntegerField(blank=True, default=0, null=True)),
                ('away_half_score', models.IntegerField(blank=True, default=0, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal_du_match', to='fixtureApp.match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_du_goal', to='teamApp.team')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
