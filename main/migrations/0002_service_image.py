# Generated by Django 5.1.3 on 2024-11-11 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(default='services/default_service.png', upload_to='services/'),
        ),
    ]
