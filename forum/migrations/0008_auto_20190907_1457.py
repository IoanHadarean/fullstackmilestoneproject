# Generated by Django 2.2.4 on 2019-09-07 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_auto_20190813_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created_date']},
        ),
    ]