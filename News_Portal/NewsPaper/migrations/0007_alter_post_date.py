# Generated by Django 5.0.1 on 2024-02-07 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPaper', '0006_alter_author_rating_alter_category_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата'),
        ),
    ]
