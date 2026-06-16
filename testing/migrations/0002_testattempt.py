# Generated manually for the local SQL AI Tutor history model.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="difficulty",
            field=models.CharField(
                choices=[
                    ("easy", "Легкий"),
                    ("medium", "Средний"),
                    ("hard", "Сложный"),
                ],
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="TestAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("student_name", models.CharField(max_length=255)),
                ("group_name", models.CharField(max_length=100)),
                (
                    "topic",
                    models.CharField(
                        choices=[
                            ("postgresql", "PostgreSQL"),
                            ("dbeaver", "DBeaver"),
                            ("northwind", "Northwind"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("easy", "Легкий"),
                            ("medium", "Средний"),
                            ("hard", "Сложный"),
                        ],
                        max_length=20,
                    ),
                ),
                ("score", models.FloatField()),
                ("level", models.CharField(max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
