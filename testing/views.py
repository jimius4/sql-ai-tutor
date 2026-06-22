from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .agent import SQLTutorAgent
from .forms import StartTestForm
from .models import TestAttempt
from .question_generator import (
    DIFFICULTY_LABELS,
    TOPIC_DML,
    TOPIC_LABELS,
    check_answers,
    generate_test,
)


def home(request):
    if request.method == "POST":
        form = StartTestForm(request.POST)

        if form.is_valid():
            agent = SQLTutorAgent()
            student_name = form.cleaned_data["full_name"].strip()
            group_name = form.cleaned_data["group_name"].strip()
            topic = TOPIC_DML

            last_attempt = (
                TestAttempt.objects.filter(
                    student_name__iexact=student_name,
                    group_name__iexact=group_name,
                    topic=topic,
                )
                .order_by("-created_at")
                .first()
            )
            agent_plan = agent.plan_test(last_attempt)
            difficulty = agent_plan["difficulty"]
            question_count = agent_plan["questions_count"]
            questions = generate_test(topic, difficulty, question_count)

            if not questions:
                form.add_error(None, "Для темы «ЯЗЫК DML» пока нет вопросов.")
            else:
                request.session["current_questions"] = questions
                request.session["current_test"] = {
                    "student_name": student_name,
                    "group_name": group_name,
                    "topic": topic,
                    "topic_label": TOPIC_LABELS[topic],
                    "difficulty": difficulty,
                    "difficulty_label": DIFFICULTY_LABELS[difficulty],
                    "mode": "agent",
                    "mode_label": "ИИ-агент",
                    "agent_plan": agent_plan,
                    "question_count": len(questions),
                    "pass_percent": agent.PASS_PERCENT,
                }

                return render(
                    request,
                    "test.html",
                    {
                        "questions": questions,
                        "test_info": request.session["current_test"],
                    },
                )
    else:
        form = StartTestForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
            "topic_label": TOPIC_LABELS[TOPIC_DML],
            "pass_percent": SQLTutorAgent.PASS_PERCENT,
        },
    )


@require_POST
def finish_test(request):
    questions = request.session.get("current_questions")
    test_info = request.session.get("current_test")

    if not questions or not test_info:
        messages.error(request, "Тест не найден. Начните новое прохождение.")
        return redirect("home")

    result = check_answers(request.POST, questions)
    agent = SQLTutorAgent()
    report = agent.create_learning_report(
        result["score_percent"],
        current_difficulty=test_info["difficulty"],
    )

    attempt = TestAttempt.objects.create(
        student_name=test_info["student_name"],
        group_name=test_info["group_name"],
        topic=test_info["topic"],
        difficulty=test_info["difficulty"],
        score=result["score_percent"],
        level=report["level"],
    )

    request.session.pop("current_questions", None)
    request.session.pop("current_test", None)

    return render(
        request,
        "result.html",
        {
            "attempt": attempt,
            "test_info": test_info,
            "result": result,
            "report": report,
        },
    )


def statistics(request):
    attempts = TestAttempt.objects.all()
    total_tests = attempts.count()
    average_score = attempts.aggregate(value=Avg("score"))["value"] or 0
    students_count = (
        attempts.values("student_name", "group_name")
        .distinct()
        .count()
    )
    level_distribution = attempts.values("level").annotate(count=Count("id")).order_by("level")
    recent_attempts = attempts[:10]

    return render(
        request,
        "statistics.html",
        {
            "total_tests": total_tests,
            "average_score": round(average_score, 1),
            "students_count": students_count,
            "level_distribution": level_distribution,
            "recent_attempts": recent_attempts,
        },
    )


def demo_agent(request):
    agent = SQLTutorAgent()
    report = agent.create_learning_report(72, current_difficulty="easy")

    return render(
        request,
        "result.html",
        {
            "attempt": None,
            "test_info": {
                "student_name": "Демо-студент",
                "group_name": "Демо",
                "topic_label": "ЯЗЫК DML",
                "difficulty_label": "Легкий",
                "mode_label": "ИИ-агент",
                "pass_percent": agent.PASS_PERCENT,
            },
            "result": {
                "total": 0,
                "correct_count": 0,
                "incorrect_count": 0,
                "score_percent": report["score"],
                "score_percent_width": str(report["score"]),
                "details": [],
            },
            "report": report,
        },
    )
