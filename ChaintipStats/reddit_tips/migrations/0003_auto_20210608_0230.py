# Generated by Django 3.2.4 on 2021-06-08 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_tips', '0002_auto_20210608_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reddittip',
            name='claimed',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='reddittip',
            name='returned',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='reddittip',
            name='sent',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
