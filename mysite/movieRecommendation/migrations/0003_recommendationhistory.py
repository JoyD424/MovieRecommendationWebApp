# Generated by Django 2.2 on 2019-05-14 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieRecommendation', '0002_auto_20190510_2359'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField(default=0)),
                ('recommendations', models.CharField(max_length=50000)),
            ],
        ),
    ]
