# Generated by Django 3.0.6 on 2020-07-03 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('names', '0004_auto_20200630_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='midname',
            name='thanh',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]