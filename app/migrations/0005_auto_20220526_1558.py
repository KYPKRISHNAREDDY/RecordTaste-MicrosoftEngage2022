# Generated by Django 3.2 on 2022-05-26 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220526_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chefs_preparing_product',
            name='title',
        ),
        migrations.AlterField(
            model_name='chefs_preparing_product',
            name='pdtid',
            field=models.ForeignKey(db_column='title', on_delete=django.db.models.deletion.CASCADE, to='app.product', to_field='title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
