import random


class SQLTutorAgent:
    LEVEL_EASY = "Легкий"
    LEVEL_MEDIUM = "Средний"
    LEVEL_HARD = "Сложный"
    PASS_PERCENT = 70

    DIFFICULTY_TO_LEVEL = {
        "easy": LEVEL_EASY,
        "medium": LEVEL_MEDIUM,
        "hard": LEVEL_HARD,
    }

    LEVEL_TO_DIFFICULTY = {
        LEVEL_EASY: "easy",
        LEVEL_MEDIUM: "medium",
        LEVEL_HARD: "hard",
    }

    QUESTION_COUNTS = {
        "easy": 5,
        "medium": 7,
        "hard": 10,
    }

    def __init__(self):
        self.student_level = self.LEVEL_EASY

    def analyze_result(self, score_percent):
        if score_percent >= 85:
            self.student_level = self.LEVEL_HARD
        elif score_percent >= self.PASS_PERCENT:
            self.student_level = self.LEVEL_MEDIUM
        else:
            self.student_level = self.LEVEL_EASY

        return self.student_level

    def plan_test(self, last_attempt=None):
        difficulty = self.choose_initial_difficulty(last_attempt)
        self.student_level = self.DIFFICULTY_TO_LEVEL[difficulty]

        return {
            "difficulty": difficulty,
            "level": self.student_level,
            "questions_count": self.choose_question_count(difficulty),
            "pass_percent": self.PASS_PERCENT,
            "reason": self._plan_reason(last_attempt, difficulty),
        }

    def choose_initial_difficulty(self, last_attempt=None):
        if last_attempt is None:
            return "easy"

        if last_attempt.score < self.PASS_PERCENT:
            return last_attempt.difficulty

        if last_attempt.difficulty == "easy":
            return "medium"

        if last_attempt.difficulty == "medium":
            return "hard"

        return "hard"

    def choose_next_difficulty(self, current_difficulty, score_percent):
        if score_percent < self.PASS_PERCENT:
            return current_difficulty

        if current_difficulty == "easy":
            return "medium"

        if current_difficulty == "medium":
            return "hard"

        return "hard"

    def choose_question_count(self, difficulty=None):
        difficulty = difficulty or self.LEVEL_TO_DIFFICULTY.get(self.student_level, "easy")
        return self.QUESTION_COUNTS.get(difficulty, self.QUESTION_COUNTS["easy"])

    def recommend_topics(self):
        topics = {
            self.LEVEL_EASY: [
                "Назначение команд DML",
                "SELECT и базовая фильтрация WHERE",
                "INSERT INTO для добавления строк",
            ],
            self.LEVEL_MEDIUM: [
                "UPDATE с безопасным WHERE",
                "DELETE и проверка строк перед удалением",
                "Агрегаты и группировка в DML-запросах",
            ],
            self.LEVEL_HARD: [
                "INSERT INTO ... SELECT",
                "UPDATE с подзапросами",
                "Транзакции при массовом изменении данных",
            ],
        }
        return topics[self.student_level]

    def generate_recommendation(self, current_difficulty=None, score_percent=None):
        recommendations = {
            self.LEVEL_EASY: [
                "Повторите, какие команды входят в DML: SELECT, INSERT, UPDATE и DELETE.",
                "Отработайте простые условия WHERE, чтобы выбирать только нужные строки.",
                "Перед изменением данных сначала проверяйте выборку через SELECT.",
            ],
            self.LEVEL_MEDIUM: [
                "Закрепите UPDATE и DELETE с обязательным условием WHERE.",
                "Потренируйтесь добавлять строки через INSERT и проверять результат SELECT-запросом.",
                "Разберите группировку данных через GROUP BY для анализа результатов.",
            ],
            self.LEVEL_HARD: [
                "Переходите к DML-запросам с подзапросами и связями между таблицами.",
                "Используйте транзакции для безопасного выполнения нескольких изменений.",
                "Пробуйте массовые операции INSERT INTO ... SELECT и UPDATE по результату подзапроса.",
            ],
        }

        result = list(recommendations[self.student_level])
        if current_difficulty and score_percent is not None:
            next_difficulty = self.choose_next_difficulty(current_difficulty, score_percent)
            if next_difficulty == current_difficulty and score_percent < self.PASS_PERCENT:
                result.append(
                    f"Для перехода дальше нужно набрать минимум {self.PASS_PERCENT}%. "
                    "Агент оставит этот же уровень для повторения."
                )
            elif next_difficulty != current_difficulty:
                result.append("Уровень пройден. В следующем тесте агент переведет вас на следующий уровень.")
            else:
                result.append("Сложный уровень пройден. Дальше можно закреплять DML на практических задачах.")

        return result

    def generate_next_topic(self):
        next_topics = {
            self.LEVEL_EASY: [
                "SELECT и WHERE",
                "INSERT INTO",
                "Безопасная проверка данных перед изменением",
            ],
            self.LEVEL_MEDIUM: [
                "UPDATE и DELETE",
                "GROUP BY в DML-задачах",
                "Изменение данных по условию",
            ],
            self.LEVEL_HARD: [
                "DML с подзапросами",
                "INSERT INTO ... SELECT",
                "Транзакции и откат изменений",
            ],
        }
        return random.choice(next_topics[self.student_level])

    def generate_practical_task(self):
        tasks = {
            self.LEVEL_EASY: [
                "В учебной таблице products выберите товары дороже 100 и отсортируйте их по цене.",
                "Добавьте одну тестовую запись в таблицу students через INSERT INTO и проверьте ее SELECT-запросом.",
                "Выведите строки из таблицы orders только за выбранную дату с помощью WHERE.",
            ],
            self.LEVEL_MEDIUM: [
                "Обновите статус тестовой записи через UPDATE с точным WHERE и проверьте результат SELECT-запросом.",
                "Перед DELETE выполните SELECT с тем же условием, затем удалите только найденную тестовую запись.",
                "Сгруппируйте заказы по статусу и посчитайте количество строк в каждой группе.",
            ],
            self.LEVEL_HARD: [
                "Выполните INSERT INTO ... SELECT, чтобы перенести выбранные тестовые строки в архивную таблицу.",
                "Обновите строки через UPDATE с подзапросом, предварительно проверив набор строк через SELECT.",
                "Оберните несколько DML-операций в транзакцию и проверьте сценарий COMMIT и ROLLBACK.",
            ],
        }
        return random.choice(tasks[self.student_level])

    def _plan_reason(self, last_attempt, difficulty):
        level = self.DIFFICULTY_TO_LEVEL[difficulty]

        if last_attempt is None:
            return "Это первое прохождение по теме «ЯЗЫК DML», поэтому агент начинает с легкого уровня."

        if last_attempt.score < self.PASS_PERCENT:
            return (
                f"Предыдущий результат {last_attempt.score}% ниже проходного порога "
                f"{self.PASS_PERCENT}%, поэтому агент оставляет уровень «{level}»."
            )

        if last_attempt.difficulty == "hard":
            return "Сложный уровень уже пройден, агент оставляет сложный тест для закрепления."

        return f"Предыдущий уровень пройден, агент переводит вас на уровень «{level}»."

    def create_learning_report(self, score_percent, current_difficulty="easy"):
        level = self.analyze_result(score_percent)
        next_difficulty = self.choose_next_difficulty(current_difficulty, score_percent)
        next_level = self.DIFFICULTY_TO_LEVEL[next_difficulty]

        return {
            "score": score_percent,
            "level": level,
            "recommendations": self.generate_recommendation(current_difficulty, score_percent),
            "recommendation": "\n".join(self.generate_recommendation(current_difficulty, score_percent)),
            "recommended_topics": self.recommend_topics(),
            "next_topic": self.generate_next_topic(),
            "practical_task": self.generate_practical_task(),
            "questions_count": self.choose_question_count(next_difficulty),
            "next_difficulty": next_difficulty,
            "next_level": next_level,
            "pass_percent": self.PASS_PERCENT,
        }
