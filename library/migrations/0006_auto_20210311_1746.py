# Generated by Django 3.1.2 on 2021-03-11 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20210311_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookloan',
            name='status',
            field=models.SmallIntegerField(default=0),
        ),
    ]