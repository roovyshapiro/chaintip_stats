# Generated by Django 3.2.4 on 2021-06-08 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RedditTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blockchain_tx', models.CharField(max_length=150)),
                ('coin_amount', models.FloatField()),
                ('coin_type', models.CharField(max_length=10)),
                ('fiat_type', models.CharField(max_length=10)),
                ('fiat_value', models.FloatField()),
                ('receiver', models.CharField(max_length=30)),
                ('sender', models.CharField(max_length=30)),
                ('body_text', models.TextField()),
                ('created_datetime', models.DateTimeField(null=True)),
                ('created_utc', models.FloatField()),
                ('comment_id', models.CharField(max_length=15)),
                ('parent_comment_permalink', models.CharField(max_length=150)),
                ('parent_id', models.CharField(max_length=15)),
                ('permalink', models.CharField(max_length=150)),
                ('score', models.IntegerField()),
                ('subreddit', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
