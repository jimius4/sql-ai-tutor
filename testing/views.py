from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .agent import SQLTutorAgent
from .forms import StartTestForm
from .models import TestAttempt
from .question_generator import (
    DIFFICULTY_LABELS,
    TOPIC_LABELS,
    check_answers,
    generate_test,
)


def home(request):
    if request.method == "POST":
        form = StartTestForm(request.POST)

        if form.is_valid():
            agent = SQLTutorAgent()
            full_name = form.cleaned_data["full_name"].strip()
            group_name = form.cleaned_data["group_name"].strip()
            topic = form.cleaned_data["topic"]
            mode = form.cleaned_data["mode"]
            difficulty = form.cleaned_data["difficulty"]
            agent_plan = None

            if mode == "agent":
                last_attempt = (
                    TestAttempt.objects.filter(
                        student_name__iexact=full_name,
                        group_name__iexact=group_name,
                        topic=topic,
                    )
                    .order_by("-created_at")
                    .first()
                )
                previous_score = last_attempt.score if last_attempt else None
                agent_plan = agent.plan_test(previous_score)
                difficulty = agent_plan["difficulty"]
                question_count = agent_plan["questions_count"]
            else:
                question_count = agent.question_count_for_difficulty(difficulty)

            questions = generate_test(topic, difficulty, question_count)

            if not questions:
                form.add_error(None, "Для выбранной темы пока нет вопросов.")
            else:
                request.session["current_questions"] = questions
                request.session["current_test"] = {
                    "student_name": full_name,
                    "group_name": group_name,
                    "topic": topic,
                    "topic_label": TOPIC_LABELS.get(topic, topic),
                    "difficulty": difficulty,
                    "difficulty_label": DIFFICULTY_LABELS.get(difficulty, difficulty),
                    "mode": mode,
                    "mode_label": "ИИ-агент" if mode == "agent" else "Стандартный тест",
                    "agent_plan": agent_plan,
                    "question_count": len(questions),
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

    return render(request, "home.html", {"form": form})


@require_POST
def finish_test(request):
    questions = request.session.get("current_questions")
    test_info = request.session.get("current_test")

    if not questions or not test_info:
        messages.error(request, "Тест не найден. Начните новое прохождение.")
        return redirect("home")

    result = check_answers(request.POST, questions)
    agent = SQLTutorAgent()
    report = agent.create_learning_report(result["score_percent"])

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
    report = agent.create_learning_report(72)

    return render(
        request,
        "result.html",
        {
            "attempt": None,
            "test_info": {
                "student_name": "Демо-студент",
                "group_name": "Демо",
                "topic_label": "PostgreSQL",
                "difficulty_label": "Средний",
                "mode_label": "ИИ-агент",
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
