# Generated by Django 3.1.1 on 2020-10-10 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creator',
            name='nickname',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='creator',
            name='phone_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
