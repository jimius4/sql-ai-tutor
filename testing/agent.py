import random


class SQLTutorAgent:
    LEVEL_EASY = "Легкий"
    LEVEL_MEDIUM = "Средний"
    LEVEL_HARD = "Сложный"

    def __init__(self):
        self.student_level = self.LEVEL_EASY

    def analyze_result(self, score_percent):
        """Определяет уровень студента по проценту выполнения теста."""
        if score_percent >= 80:
            self.student_level = self.LEVEL_HARD
        elif score_percent >= 50:
            self.student_level = self.LEVEL_MEDIUM
        else:
            self.student_level = self.LEVEL_EASY

        return self.student_level

    def recommend_topics(self):
        topics = {
            self.LEVEL_EASY: [
                "SELECT, WHERE и сортировка результатов",
                "Агрегатные функции COUNT, SUM, AVG",
                "Навигация по подключению в DBeaver",
            ],
            self.LEVEL_MEDIUM: [
                "INNER JOIN и LEFT JOIN",
                "GROUP BY и HAVING",
                "Первичные и внешние ключи в Northwind",
            ],
            self.LEVEL_HARD: [
                "CTE и подзапросы",
                "Оконные функции",
                "Индексы и анализ плана выполнения EXPLAIN",
            ],
        }
        return topics[self.student_level]

    def generate_recommendation(self):
        recommendations = {
            self.LEVEL_EASY: [
                "Закрепите базовый синтаксис SELECT и фильтрацию строк.",
                "Потренируйтесь читать структуру таблиц Customers, Orders и Products.",
                "В DBeaver повторите подключение к базе и запуск простых запросов.",
            ],
            self.LEVEL_MEDIUM: [
                "Сфокусируйтесь на связях таблиц и разных типах JOIN.",
                "Решайте задачи на группировку заказов, клиентов и товаров.",
                "Проверяйте запросы в DBeaver через вкладки результата и истории выполнения.",
            ],
            self.LEVEL_HARD: [
                "Переходите к аналитическим запросам с CTE и оконными функциями.",
                "Изучите EXPLAIN ANALYZE и влияние индексов на запросы.",
                "Пробуйте писать запросы, которые объединяют продажи, товары, клиентов и сотрудников.",
            ],
        }
        return recommendations[self.student_level]

    def choose_question_count(self):
        question_counts = {
            self.LEVEL_EASY: 5,
            self.LEVEL_MEDIUM: 7,
            self.LEVEL_HARD: 10,
        }
        return question_counts[self.student_level]

    def question_count_for_difficulty(self, difficulty):
        counts = {
            "easy": 5,
            "medium": 7,
            "hard": 10,
        }
        return counts.get(difficulty, 5)

    def choose_next_difficulty(self):
        difficulties = {
            self.LEVEL_EASY: "easy",
            self.LEVEL_MEDIUM: "medium",
            self.LEVEL_HARD: "hard",
        }
        return difficulties[self.student_level]

    def choose_initial_difficulty(self, previous_score=None):
        if previous_score is None:
            return "medium"
        if previous_score >= 80:
            return "hard"
        if previous_score >= 50:
            return "medium"
        return "easy"

    def generate_practical_task(self):
        tasks = {
            self.LEVEL_EASY: [
                "В базе Northwind выведите названия всех товаров из таблицы Products и отсортируйте их по цене.",
                "Найдите всех клиентов из таблицы Customers, у которых страна равна Germany.",
                "Посчитайте количество заказов в таблице Orders.",
            ],
            self.LEVEL_MEDIUM: [
                "Покажите клиентов и количество их заказов, используя Customers и Orders.",
                "Найдите категории товаров и среднюю цену товара в каждой категории.",
                "Выведите сотрудников и количество заказов, которые они обработали.",
            ],
            self.LEVEL_HARD: [
                "С помощью CTE найдите топ-5 клиентов по сумме заказов.",
                "Используйте оконную функцию, чтобы ранжировать товары внутри каждой категории по цене.",
                "Сравните план выполнения запроса до и после добавления индекса на внешний ключ.",
            ],
        }
        return random.choice(tasks[self.student_level])

    def generate_next_topic(self):
        next_topics = {
            self.LEVEL_EASY: [
                "Фильтрация данных WHERE",
                "Сортировка ORDER BY",
                "Агрегатные функции",
            ],
            self.LEVEL_MEDIUM: [
                "JOIN в схеме Northwind",
                "GROUP BY и HAVING",
                "Связи таблиц и ключи",
            ],
            self.LEVEL_HARD: [
                "CTE и подзапросы",
                "Оконные функции PostgreSQL",
                "Оптимизация запросов",
            ],
        }
        return random.choice(next_topics[self.student_level])

    def plan_test(self, previous_score=None):
        difficulty = self.choose_initial_difficulty(previous_score)
        level_by_difficulty = {
            "easy": self.LEVEL_EASY,
            "medium": self.LEVEL_MEDIUM,
            "hard": self.LEVEL_HARD,
        }
        self.student_level = level_by_difficulty[difficulty]

        return {
            "difficulty": difficulty,
            "questions_count": self.choose_question_count(),
            "reason": self._plan_reason(previous_score),
        }

    def _plan_reason(self, previous_score):
        if previous_score is None:
            return "Истории прохождения пока нет, поэтому агент начинает со среднего уровня."
        if previous_score >= 80:
            return "Предыдущий результат высокий, агент повышает сложность."
        if previous_score >= 50:
            return "Предыдущий результат уверенный, агент оставляет средний уровень."
        return "Предыдущий результат требует закрепления базы, агент выбирает легкий уровень."

    def create_learning_report(self, score_percent):
        level = self.analyze_result(score_percent)

        return {
            "score": score_percent,
            "level": level,
            "recommendations": self.generate_recommendation(),
            "recommendation": "\n".join(self.generate_recommendation()),
            "recommended_topics": self.recommend_topics(),
            "next_topic": self.generate_next_topic(),
            "practical_task": self.generate_practical_task(),
            "questions_count": self.choose_question_count(),
            "next_difficulty": self.choose_next_difficulty(),
        }
