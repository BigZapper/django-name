# Generated by Django 3.0.6 on 2020-07-03 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('names', '0005_midname_thanh'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='thanh',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]