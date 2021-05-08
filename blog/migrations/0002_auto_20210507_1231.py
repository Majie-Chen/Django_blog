# Generated by Django 3.2 on 2021-05-07 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_time'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AlterModelOptions(
            name='blogtype',
            options={'verbose_name': '文章类型', 'verbose_name_plural': '文章类型'},
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='blog.blogtype', verbose_name='文章类型'),
        ),
        migrations.AlterField(
            model_name='blogtype',
            name='type_name',
            field=models.CharField(max_length=15, verbose_name='文章类型'),
        ),
    ]
