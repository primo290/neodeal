# Generated by Django 4.2.16 on 2024-12-31 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_customuser_revenu_customuser_solde'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip',
            name='url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
