# Generated by Django 4.1.1 on 2022-11-08 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_shop', '0003_alter_productitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=50),
        ),
    ]
