from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("testing", "0002_testattempt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="topic",
            field=models.CharField(
                choices=[
                    ("dml", "ЯЗЫК DML"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="testattempt",
            name="topic",
            field=models.CharField(
                choices=[
                    ("dml", "ЯЗЫК DML"),
                ],
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="testattempt",
            name="attempt_number",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="testattempt",
            name="best_score",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="testattempt",
            name="duration_minutes",
            field=models.PositiveIntegerField(default=25),
        ),
        migrations.CreateModel(
            name="TestAnswer",
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
                ("question_number", models.PositiveIntegerField()),
                ("question_text", models.TextField()),
                ("selected_answer_index", models.PositiveIntegerField(blank=True, null=True)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "attempt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="testing.testattempt",
                    ),
                ),
            ],
            options={
                "ordering": ["question_number"],
            },
        ),
    ]
