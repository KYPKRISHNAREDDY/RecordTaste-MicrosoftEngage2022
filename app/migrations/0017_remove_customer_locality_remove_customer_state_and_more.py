# Generated by Django 4.0.4 on 2022-05-28 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_rename_title_chefs_preparing_product_titleid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='locality',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='state',
        ),
        migrations.AddField(
            model_name='customer',
            name='Category',
            field=models.CharField(choices=[('Vegetarian', 'Vegetarian'), ('NonVegetarian', 'NonVegetarian')], default='Vegetarian', max_length=25),
        ),
        migrations.AlterField(
            model_name='customer',
            name='prefers',
            field=models.CharField(choices=[('Chinese', 'Chinese'), ('Italian', 'Italian'), ('Indian', 'Indian'), ('others', 'others')], default='Indian', max_length=50),
        ),
    ]
