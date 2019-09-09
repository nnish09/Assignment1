# Generated by Django 2.2.5 on 2019-09-04 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reglogprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='profimg',
            field=models.ImageField(default='img/logo.png', upload_to='images/'),
        ),
    ]
