# Generated by Django 2.2.3 on 2019-08-03 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190803_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='static/img/default.jpeg', upload_to=''),
        ),
    ]
