# Generated by Django 2.2.6 on 2019-10-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainees', '0005_physical_attribute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='physical_attribute',
            name='handstand',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=8),
        ),
    ]