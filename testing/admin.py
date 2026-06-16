from django.contrib import admin

from .models import Question, Student, TestAttempt, TestResult


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "group_name")
    search_fields = ("full_name", "group_name")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "topic", "difficulty", "correct_answer")
    list_filter = ("topic", "difficulty")
    search_fields = ("question_text",)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("student", "topic", "score", "created_at")
    list_filter = ("topic", "created_at")
    search_fields = ("student__full_name",)


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "group_name",
        "topic",
        "difficulty",
        "score",
        "level",
        "created_at",
    )
    list_filter = ("topic", "difficulty", "level", "created_at")
    search_fields = ("student_name", "group_name")
