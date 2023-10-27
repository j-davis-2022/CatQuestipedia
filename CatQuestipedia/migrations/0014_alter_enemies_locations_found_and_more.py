# Generated by Django 4.2.4 on 2023-10-26 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatQuestipedia', '0013_alter_game_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enemies',
            name='locations_found',
            field=models.ManyToManyField(blank=True, to='CatQuestipedia.locations'),
        ),
        migrations.AlterField(
            model_name='locations',
            name='enemies_there',
            field=models.ManyToManyField(blank=True, to='CatQuestipedia.enemies'),
        ),
        migrations.AlterField(
            model_name='locations',
            name='type',
            field=models.CharField(choices=[('cave', 'Cave'), ('ruins', 'Ruins'), ('town', 'Town'), ('overworld', 'Overworld')], max_length=9),
        ),
    ]