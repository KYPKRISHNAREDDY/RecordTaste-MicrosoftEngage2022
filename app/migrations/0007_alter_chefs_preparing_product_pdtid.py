# Generated by Django 3.2 on 2022-05-26 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_chefs_preparing_product_pdtid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chefs_preparing_product',
            name='pdtid',
            field=models.ForeignKey(db_column='title', on_delete=django.db.models.deletion.CASCADE, to='app.product', to_field='title'),
        ),
    ]
