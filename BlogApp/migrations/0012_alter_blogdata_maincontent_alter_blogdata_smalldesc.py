# Generated by Django 4.1 on 2022-08-29 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0011_alter_blogdata_image_alter_blogdata_maincontent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogdata',
            name='maincontent',
            field=models.CharField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='blogdata',
            name='smalldesc',
            field=models.CharField(max_length=500),
        ),
    ]
