# Generated by Django 4.1.4 on 2022-12-28 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_key', models.CharField(max_length=10, unique=True)),
                ('item_value', models.IntegerField(default=1)),
            ],
        ),
    ]
