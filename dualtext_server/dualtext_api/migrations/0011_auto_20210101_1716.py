# Generated by Django 3.1.3 on 2021-01-01 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dualtext_api', '0010_auto_20201207_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='is_reviewed',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='annotator_labels',
            field=models.ManyToManyField(blank=True, related_name='annotation_annotator', to='dualtext_api.Label'),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='reviewer_labels',
            field=models.ManyToManyField(blank=True, related_name='annotation_reviewer', to='dualtext_api.Label'),
        ),
    ]
