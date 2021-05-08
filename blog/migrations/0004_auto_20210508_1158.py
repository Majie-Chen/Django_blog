# Generated by Django 3.2 on 2021-05-08 11:58

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='readed_num',
            field=models.IntegerField(default=0, verbose_name='访问人数'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='正文'),
        ),
    ]
