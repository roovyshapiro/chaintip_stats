# Generated by Django 3.2.4 on 2021-08-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_tips', '0005_bchprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='reddittip',
            name='unclaimed',
            field=models.BooleanField(default=None, null=True),
        ),
    ]