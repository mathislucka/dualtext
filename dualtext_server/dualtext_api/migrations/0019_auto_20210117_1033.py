# Generated by Django 3.1.3 on 2021-01-17 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dualtext_api', '0018_auto_20210116_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='corpus',
        ),
        migrations.AddField(
            model_name='feature',
            name='corpora',
            field=models.ManyToManyField(blank=True, to='dualtext_api.Corpus'),
        ),
    ]