# Generated by Django 4.1.4 on 2022-12-29 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verified_puppers', '0002_alter_dog_original_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='original_img_url',
            field=models.URLField(),
        ),
    ]
