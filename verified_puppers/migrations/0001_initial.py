# Generated by Django 4.1.4 on 2022-12-29 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_img', models.URLField(unique=True)),
                ('modified_img', models.JSONField(null=True)),
                ('img_width', models.IntegerField(null=True)),
                ('img_height', models.IntegerField(null=True)),
                ('img_aspect_ratio', models.FloatField(null=True)),
                ('img_format', models.CharField(max_length=10, null=True)),
                ('img_mode', models.CharField(max_length=10, null=True)),
                ('is_img_animated', models.BooleanField(null=True)),
                ('frames_in_img', models.IntegerField(null=True)),
                ('img_exifdata', models.JSONField(null=True)),
            ],
        ),
    ]