# Generated by Django 3.0.6 on 2020-06-16 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('names', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]