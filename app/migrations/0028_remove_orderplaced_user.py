# Generated by Django 4.0.4 on 2022-05-28 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_orderplaced_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='user',
        ),
    ]
