# Generated by Django 2.2.6 on 2019-10-22 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0008_shape_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shape_state',
            old_name='previous_levl',
            new_name='previous_level',
        ),
    ]