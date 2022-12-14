# Generated by Django 4.1.4 on 2022-12-24 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fixtureApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['date', 'hour', 'home']},
        ),
        migrations.AddField(
            model_name='match',
            name='is_first_match',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
