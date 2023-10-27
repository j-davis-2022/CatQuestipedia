# Generated by Django 4.2.4 on 2023-10-23 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatQuestipedia', '0010_test'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.AddField(
            model_name='enemies',
            name='enemy',
            field=models.ImageField(blank=True, null=True, upload_to='enemies'),
        ),
        migrations.AlterField(
            model_name='characters',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='characters'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='equipment'),
        ),
        migrations.AlterField(
            model_name='spells',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='spells'),
        ),
    ]