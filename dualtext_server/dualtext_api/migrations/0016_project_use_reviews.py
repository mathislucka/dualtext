# Generated by Django 3.1.3 on 2021-01-08 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dualtext_api', '0015_auto_20210108_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='use_reviews',
            field=models.BooleanField(blank=True, default=True),
        ),
    ]
