# Generated by Django 4.1.1 on 2022-11-01 22:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
    ]
