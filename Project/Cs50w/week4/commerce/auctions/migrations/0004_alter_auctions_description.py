# Generated by Django 4.1 on 2022-09-06 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_auctions_category_auctions_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctions',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]