# Generated by Django 5.0 on 2024-05-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0004_user_reg_img_delete_pricing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_reg',
            name='img',
            field=models.ImageField(default='/static/media/arlacchino_badass_edit-Cover_RlOWyJ1.jpg', null=True, upload_to='profile-image/'),
        ),
    ]