from .question_generator import TOPIC_DML, generate_test


def generate_ai_questions(topic=TOPIC_DML, level="easy", question_count=15):
    """Локальный генератор вопросов без внешних API."""
    return generate_test(topic, level, question_count)
