# Generated by Django 3.0.8 on 2021-02-09 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seat',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]