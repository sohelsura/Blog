# Generated by Django 4.1 on 2022-08-26 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0002_usersregistered'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersregistered',
            name='image',
            field=models.ImageField(null='True', upload_to='userimage'),
            preserve_default='True',
        ),
    ]
