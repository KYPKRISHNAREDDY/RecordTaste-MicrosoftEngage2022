# Generated by Django 4.0.4 on 2022-05-28 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_customer_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
