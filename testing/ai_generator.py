from .question_generator import generate_test


def generate_ai_questions(topic, level, question_count=5):
    """Локальная совместимая замена прежнего внешнего AI-генератора."""
    return generate_test(topic, level, question_count)
