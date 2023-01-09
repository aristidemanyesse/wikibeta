# Generated by Django 4.1.4 on 2023-01-07 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitionApp', '0005_ranking_ligneranking'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='editioncompetition',
            options={'ordering': ['competition', '-start_date']},
        ),
        migrations.RemoveField(
            model_name='ranking',
            name='start_date',
        ),
        migrations.AddField(
            model_name='competition',
            name='logo',
            field=models.ImageField(blank=True, default='', max_length=255, null=True, upload_to='static/images/competitions/'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_de_competition', to='competitionApp.typecompetition'),
        ),
    ]
