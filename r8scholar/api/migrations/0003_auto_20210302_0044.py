# Generated by Django 3.1.6 on 2021-03-02 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210302_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='verification_code',
            field=models.CharField(default='18DVUW', max_length=10),
        ),
    ]
