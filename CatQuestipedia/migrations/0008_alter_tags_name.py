# Generated by Django 4.2.4 on 2023-10-23 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatQuestipedia', '0007_characters_tags_enemies_tags_equipment_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
