# Generated by Django 4.1.5 on 2023-12-14 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follows_likes_post'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Likes',
            new_name='Follow',
        ),
        migrations.RenameModel(
            old_name='Follows',
            new_name='Like',
        ),
    ]
