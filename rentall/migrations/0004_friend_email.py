# Generated by Django 4.0.2 on 2022-02-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentall', '0003_friend_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]