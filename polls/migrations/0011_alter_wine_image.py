# Generated by Django 4.2.7 on 2024-11-22 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_alter_winescore_session_wine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wine',
            name='image',
            field=models.BinaryField(),
        ),
    ]
