# Generated by Django 3.1.5 on 2021-02-07 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('r8scholar', '0010_auto_20210207_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='id',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='r8scholar.subject'),
        ),
    ]
