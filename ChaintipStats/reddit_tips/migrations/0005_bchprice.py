# Generated by Django 3.2.4 on 2021-06-09 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_tips', '0004_alter_reddittip_coin_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='BCHPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=30)),
                ('price_format', models.FloatField()),
                ('time', models.CharField(max_length=30)),
                ('time_dt', models.DateTimeField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
