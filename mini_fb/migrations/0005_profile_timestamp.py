# Generated by Django 5.1.2 on 2024-10-28 22:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mini_fb", "0004_friend"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="timestamp",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
