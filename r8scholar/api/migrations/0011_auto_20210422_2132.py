# Generated by Django 3.1.5 on 2021-04-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20210422_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='verification_code',
            field=models.CharField(default='IGX6UH', max_length=10),
        ),
    ]
