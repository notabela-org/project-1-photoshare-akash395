# Generated by Django 3.1.6 on 2021-03-08 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_pic_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='profile_pic',
            new_name='image',
        ),
    ]
