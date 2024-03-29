# Generated by Django 2.2.6 on 2019-10-24 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0014_auto_20191024_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution_list',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.Issues'),
        ),
        migrations.AlterField(
            model_name='solution_list',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.Solutions'),
        ),
        migrations.AlterField(
            model_name='trainees_health_issues',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health_app.Issues'),
        ),
        migrations.AlterField(
            model_name='trainees_health_issues',
            name='trainee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainees.Trainees'),
        ),
    ]
