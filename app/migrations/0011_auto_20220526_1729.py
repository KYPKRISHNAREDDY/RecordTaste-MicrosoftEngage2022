# Generated by Django 3.2 on 2022-05-26 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20220526_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='prefers',
            field=models.CharField(choices=[('Chinese', 'Chinese'), ('Italian', 'Italian'), ('Indian', 'Indian'), ('FastFood', 'FastFood'), ('Refreshments', 'Refreshments')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='region',
            field=models.CharField(choices=[('Chinese', 'Chinese'), ('Italian', 'Italian'), ('Indian', 'Indian'), ('FastFood', 'FastFood'), ('Refreshments', 'Refreshments')], max_length=50),
        ),
    ]
