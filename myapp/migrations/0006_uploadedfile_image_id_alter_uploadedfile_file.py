# Generated by Django 4.2.6 on 2023-11-03 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_uploadedfile_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='image_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='mosbefore/image\\PqXn2XflZE/'),
        ),
    ]