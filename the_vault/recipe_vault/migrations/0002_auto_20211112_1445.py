# Generated by Django 2.2 on 2021-11-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_vault', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='posted_by',
        ),
        migrations.AddField(
            model_name='recipe',
            name='posted_by',
            field=models.ManyToManyField(related_name='thisuser', to='recipe_vault.User'),
        ),
    ]
