# Generated by Django 3.1.3 on 2020-11-20 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('dualtext_api', '0004_auto_20201119_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='corpus',
            name='allowed_groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]