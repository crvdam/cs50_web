# Generated by Django 4.1.5 on 2023-09-19 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.CharField(default='aaa', max_length=64),
        ),
    ]
