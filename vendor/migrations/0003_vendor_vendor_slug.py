# Generated by Django 4.1.1 on 2022-11-01 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_alter_vendor_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendor_slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
