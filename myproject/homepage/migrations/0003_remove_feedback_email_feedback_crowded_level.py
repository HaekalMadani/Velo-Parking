# Generated by Django 5.0.6 on 2024-07-11 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("homepage", "0002_feedback_station_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedback",
            name="email",
        ),
        migrations.AddField(
            model_name="feedback",
            name="crowded_level",
            field=models.CharField(
                choices=[
                    ("uncrowded", "Uncrowded"),
                    ("less_crowded", "Less Crowded"),
                    ("relatively_crowded", "Relatively Crowded"),
                    ("crowded", "Crowded"),
                ],
                default="uncrowded",
                max_length=20,
            ),
        ),
    ]
