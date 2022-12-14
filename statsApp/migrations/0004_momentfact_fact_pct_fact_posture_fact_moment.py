# Generated by Django 4.1.4 on 2022-12-25 10:19

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('statsApp', '0003_typefact_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='MomentFact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('protected', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='fact',
            name='pct',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fact',
            name='posture',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fact',
            name='moment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moment_facts', to='statsApp.momentfact'),
        ),
    ]
