# Generated by Django 5.0 on 2024-05-07 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0008_user_reg_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='edit',
        ),
        migrations.DeleteModel(
            name='feedback',
        ),
    ]
