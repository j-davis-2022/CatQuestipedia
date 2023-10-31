# Generated by Django 4.2.4 on 2023-10-30 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatQuestipedia', '0017_rename_mode_name_mewgame_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='characters',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enemies',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='locations',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mewgame',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quests',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spells',
            name='user_edits',
            field=models.CharField(blank=True, null=True),
        ),
    ]
