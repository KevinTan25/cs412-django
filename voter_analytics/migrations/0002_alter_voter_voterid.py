# Generated by Django 5.1.2 on 2024-11-09 21:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("voter_analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="voterID",
            field=models.TextField(),
        ),
    ]
