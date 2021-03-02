# Generated by Django 3.1.6 on 2021-03-02 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210302_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='verification_code',
            field=models.CharField(default='XV78XN', max_length=10),
        ),
        migrations.AlterField(
            model_name='department',
            name='courses_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='department',
            name='instructors_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='department',
            name='overall_rating',
            field=models.FloatField(default=0),
        ),
    ]