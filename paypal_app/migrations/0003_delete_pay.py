# Generated by Django 4.1.4 on 2023-07-20 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal_app', '0002_pay'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pay',
        ),
    ]
