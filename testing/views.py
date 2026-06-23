from django.contrib import messages
from django.db.models import Avg, Count, Max
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
            difficulty = agent.choose_initial_difficulty(last_attempt)
            attempt_number = (
                TestAttempt.objects.filter(
                    student_name__iexact=student_name,
                    group_name__iexact=group_name,
                    topic=topic,
                    difficulty=difficulty,
                ).count()
                + 1
            )
            agent_plan = agent.plan_test(last_attempt, attempt_number)
            questions = generate_test(topic, difficulty, agent_plan["questions_count"])

            if not questions:
                form.add_error(None, "Для темы «ЯЗЫК DML» пока нет вопросов.")
            else:
                request.session["current_questions"] = questions
                request.session["current_answers"] = {}
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
                    "current_index": 0,
                    "attempt_number": attempt_number,
                    "duration_minutes": agent_plan["duration_minutes"],
                    "pass_percent": agent.PASS_PERCENT,
                    "passing_question_count": agent.passing_question_count,
                }

                return _render_current_question(request)
    else:
        form = StartTestForm()

    return render(
        request,
        "home.html",
        {
            "form": form,
            "topic_label": TOPIC_LABELS[TOPIC_DML],
            "pass_percent": SQLTutorAgent.PASS_PERCENT,
            "question_count": SQLTutorAgent.QUESTION_COUNT,
            "passing_question_count": SQLTutorAgent().passing_question_count,
        },
    )


@require_POST
def finish_test(request):
    questions = request.session.get("current_questions")
    test_info = request.session.get("current_test")

    if not questions or not test_info:
        messages.error(request, "Тест не найден. Начните новое прохождение.")
        return redirect("home")

    current_index = int(test_info.get("current_index", 0))
    answer_value = request.POST.get(f"question_{current_index}")

    if answer_value is None:
        messages.error(request, "Выберите вариант ответа, чтобы перейти к следующему вопросу.")
        return _render_current_question(request)

    current_answers = request.session.get("current_answers", {})
    current_answers[f"question_{current_index}"] = answer_value
    request.session["current_answers"] = current_answers

    if current_index + 1 < len(questions):
        test_info["current_index"] = current_index + 1
        request.session["current_test"] = test_info
        return _render_current_question(request)

    result = check_answers(current_answers, questions)
    agent = SQLTutorAgent()
    report = agent.create_learning_report(
        result["score_percent"],
        current_difficulty=test_info["difficulty"],
        attempt_number=test_info["attempt_number"],
    )

    attempt = TestAttempt.objects.create(
        student_name=test_info["student_name"],
        group_name=test_info["group_name"],
        topic=test_info["topic"],
        difficulty=test_info["difficulty"],
        score=result["score_percent"],
        level=report["level"],
    )
    best_score = (
        TestAttempt.objects.filter(
            student_name__iexact=test_info["student_name"],
            group_name__iexact=test_info["group_name"],
            topic=test_info["topic"],
        ).aggregate(value=Max("score"))["value"]
        or result["score_percent"]
    )

    request.session.pop("current_questions", None)
    request.session.pop("current_answers", None)
    request.session.pop("current_test", None)

    return render(
        request,
        "result.html",
        {
            "attempt": attempt,
            "test_info": test_info,
            "result": result,
            "report": report,
            "best_score": best_score,
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
    report = agent.create_learning_report(86.7, current_difficulty="easy", attempt_number=1)

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
                "attempt_number": 1,
                "duration_minutes": 25,
                "pass_percent": agent.PASS_PERCENT,
                "passing_question_count": agent.passing_question_count,
            },
            "result": {
                "total": agent.QUESTION_COUNT,
                "correct_count": 13,
                "incorrect_count": 2,
                "score_percent": report["score"],
                "score_percent_width": str(report["score"]),
                "details": [],
            },
            "report": report,
            "best_score": report["score"],
        },
    )


def _render_current_question(request):
    questions = request.session["current_questions"]
    test_info = request.session["current_test"]
    current_index = int(test_info.get("current_index", 0))
    current_question = questions[current_index]

    return render(
        request,
        "test.html",
        {
            "question": current_question,
            "question_index": current_index,
            "question_number": current_index + 1,
            "is_last_question": current_index + 1 == len(questions),
            "progress_percent": round(((current_index + 1) / len(questions)) * 100, 1),
            "test_info": test_info,
        },
    )
