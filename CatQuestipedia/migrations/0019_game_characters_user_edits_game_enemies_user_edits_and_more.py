# Generated by Django 4.2.4 on 2023-11-01 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatQuestipedia', '0018_characters_user_edits_enemies_user_edits_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='characters_user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='enemies_user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='equipment_user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='locations_user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='map',
            field=models.ImageField(null=True, upload_to='other'),
        ),
        migrations.AddField(
            model_name='game',
            name='mewgame_user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='quests_user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='spells_user_edits',
            field=models.CharField(blank=True, null=True),
        ),
    ]
