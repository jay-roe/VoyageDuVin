# Generated by Django 4.2.7 on 2024-11-22 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_alter_wine_full_name_alter_wine_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='color',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='wine',
            name='region',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='wine',
            name='variety',
            field=models.CharField(max_length=255),
        ),
    ]
