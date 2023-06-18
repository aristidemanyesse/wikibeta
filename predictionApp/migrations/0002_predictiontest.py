# Generated by Django 4.1.4 on 2023-02-03 23:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fixtureApp', '0007_match_is_facted'),
        ('predictionApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionTest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('pct', models.FloatField(blank=True, default=0.0, null=True)),
                ('is_checked', models.BooleanField(blank=True, null=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictiontest_match', to='fixtureApp.match')),
                ('mode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='predictiontest_mode', to='predictionApp.modeprediction')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictiontest_type', to='predictionApp.typeprediction')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]