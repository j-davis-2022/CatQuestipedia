# Generated by Django 4.2.4 on 2023-10-23 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatQuestipedia', '0012_otherimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(upload_to='games'),
        ),
    ]
