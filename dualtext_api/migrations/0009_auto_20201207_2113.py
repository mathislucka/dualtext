# Generated by Django 3.1.3 on 2020-12-07 21:13

from django.db import migrations


class Migration(migrations.Migration):
    def add_default_label_color(apps, schema_editor):
        Label = apps.get_model('dualtext_api', 'Label')
        for label in Label.objects.all():
            label.color = {'standard': '#97C0E8', 'light': '#EAF2FA'}
            label.save()

    def revert_add_default_label_color(apps, schema_editor):
        Label = apps.get_model('dualtext_api', 'Label')
        for label in Label.objects.filter(color={'standard': '#97C0E8', 'light': '#EAF2FA'}):
            label.color = None
            label.save()
    dependencies = [
        ('dualtext_api', '0008_auto_20201207_2109'),
    ]

    operations = [
        migrations.RunPython(add_default_label_color, revert_add_default_label_color)
    ]
