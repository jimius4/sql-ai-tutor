from django.db import models


TOPIC_CHOICES = [
    ("dml", "ЯЗЫК DML"),
]

DIFFICULTY_CHOICES = [
    ("easy", "Легкий"),
    ("medium", "Средний"),
    ("hard", "Сложный"),
]


class Student(models.Model):
    full_name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Question(models.Model):
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text


class TestResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.CharField(max_length=50)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class TestAttempt(models.Model):
    student_name = models.CharField(max_length=255)
    group_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    score = models.FloatField()
    level = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student_name} - {self.score}%"
