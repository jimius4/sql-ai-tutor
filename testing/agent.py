import math
import random


class SQLTutorAgent:
    LEVEL_EASY = "Легкий"
    LEVEL_MEDIUM = "Средний"
    LEVEL_HARD = "Сложный"
    LEVEL_FAILED = "Не сдал"

    QUESTION_COUNT = 15
    PASS_PERCENT = 85

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

    def __init__(self):
        self.student_level = self.LEVEL_EASY

    @property
    def passing_question_count(self):
        return math.ceil(self.QUESTION_COUNT * self.PASS_PERCENT / 100)

    def analyze_result(self, score_percent, current_difficulty="easy"):
        if score_percent < self.PASS_PERCENT:
            self.student_level = self.LEVEL_FAILED
        else:
            self.student_level = self.DIFFICULTY_TO_LEVEL.get(current_difficulty, self.LEVEL_EASY)

        return self.student_level

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

    def get_duration_minutes(self, difficulty, attempt_number):
        if difficulty == "hard":
            return 25

        durations = {
            1: 25,
            2: 20,
            3: 15,
        }
        return durations.get(min(attempt_number, 3), 15)

    def plan_test(self, last_attempt=None, attempt_number=1):
        difficulty = self.choose_initial_difficulty(last_attempt)
        self.student_level = self.DIFFICULTY_TO_LEVEL[difficulty]

        return {
            "difficulty": difficulty,
            "level": self.student_level,
            "questions_count": self.QUESTION_COUNT,
            "duration_minutes": self.get_duration_minutes(difficulty, attempt_number),
            "attempt_number": attempt_number,
            "pass_percent": self.PASS_PERCENT,
            "passing_question_count": self.passing_question_count,
            "reason": self._plan_reason(last_attempt, difficulty),
        }

    def grade_points(self, score_percent, difficulty, attempt_number):
        if score_percent < self.PASS_PERCENT:
            return None

        attempt_number = min(attempt_number, 3)
        if difficulty == "easy":
            ranges = {
                1: ((97, 75, 75), (90, 70, 74), (85, 61, 69)),
                2: ((97, 73, 73), (90, 68, 72), (85, 61, 71)),
                3: ((97, 70, 70), (90, 65, 69), (85, 61, 64)),
            }
        elif difficulty == "medium":
            ranges = {
                1: ((97, 90, 90), (90, 81, 89), (85, 76, 80)),
                2: ((97, 88, 88), (90, 82, 87), (85, 76, 79)),
                3: ((97, 86, 86), (90, 80, 85), (85, 76, 79)),
            }
        else:
            ranges = {
                1: ((98, 100, 100), (90, 95, 99), (85, 91, 94)),
                2: ((98, 100, 100), (90, 95, 99), (85, 91, 94)),
                3: ((98, 100, 100), (90, 95, 99), (85, 91, 94)),
            }

        for threshold, low, high in ranges[attempt_number]:
            if score_percent >= threshold:
                if low == high:
                    return high
                band_width = 100 - threshold
                position = min(max(score_percent - threshold, 0), band_width)
                return min(high, low + round((position / band_width) * (high - low)))

        return None

    def recommend_topics(self):
        topics = {
            self.LEVEL_EASY: [
                "DML-команды SELECT, INSERT, UPDATE, DELETE",
                "Фильтрация строк через WHERE",
                "Проверка данных перед изменением",
            ],
            self.LEVEL_MEDIUM: [
                "Безопасные UPDATE и DELETE",
                "GROUP BY и HAVING в SELECT",
                "Поиск ошибок в DML-запросах",
            ],
            self.LEVEL_HARD: [
                "INSERT INTO ... SELECT",
                "UPDATE и DELETE с подзапросами",
                "Транзакции COMMIT и ROLLBACK",
            ],
            self.LEVEL_FAILED: [
                "Базовые команды DML",
                "Условия WHERE",
                "Проверочный SELECT перед изменениями",
            ],
        }
        return topics[self.student_level]

    def generate_recommendation(self, current_difficulty, score_percent, grade_points):
        if score_percent < self.PASS_PERCENT:
            return [
                "Рекомендуется повторить материал и вернуться к тесту через 1-2 дня.",
                "Перед повторной попыткой разберите назначение SELECT, INSERT, UPDATE и DELETE.",
                "Особое внимание уделите условиям WHERE, потому что они защищают данные от случайных изменений.",
            ]

        recommendations = {
            "easy": [
                "Легкий уровень пройден. Можно переходить к применению DML-команд в более сложных ситуациях.",
                "Закрепите безопасную схему: сначала SELECT, затем UPDATE или DELETE с тем же WHERE.",
            ],
            "medium": [
                "Средний уровень пройден. Следующий шаг — DML с подзапросами и транзакциями.",
                "Повторите GROUP BY, HAVING и поиск ошибок в запросах.",
            ],
            "hard": [
                "Сложный уровень пройден. Результат можно фиксировать как итоговый.",
                "Для повышения результата до 100 можно пройти дополнительную попытку на сложном уровне.",
            ],
        }

        result = list(recommendations[current_difficulty])
        if grade_points and current_difficulty == "easy" and grade_points < 75:
            result.append("Можно пройти бонус-попытку, чтобы повысить балл легкого уровня до 75.")
        if grade_points and current_difficulty == "medium" and grade_points < 90:
            result.append("Можно пройти бонус-попытку, чтобы повысить балл среднего уровня до 90.")
        return result

    def generate_next_topic(self):
        next_topics = {
            self.LEVEL_EASY: [
                "SELECT и WHERE",
                "INSERT INTO",
                "UPDATE и DELETE с условием",
            ],
            self.LEVEL_MEDIUM: [
                "GROUP BY и HAVING",
                "DML-запросы с проверкой ошибок",
                "Изменение данных по условию",
            ],
            self.LEVEL_HARD: [
                "DML с подзапросами",
                "INSERT INTO ... SELECT",
                "Транзакции и откат изменений",
            ],
            self.LEVEL_FAILED: [
                "Повторение базовых DML-команд",
                "WHERE в SELECT, UPDATE и DELETE",
                "Безопасный порядок изменения данных",
            ],
        }
        return random.choice(next_topics[self.student_level])

    def generate_practical_task(self):
        tasks = {
            self.LEVEL_EASY: [
                "Напишите SELECT-запрос, который выбирает строки по условию WHERE, затем объясните, какие строки попадут в результат.",
                "Составьте INSERT INTO для добавления одной тестовой записи и проверьте ее отдельным SELECT-запросом.",
            ],
            self.LEVEL_MEDIUM: [
                "Найдите ошибку в UPDATE без WHERE, перепишите запрос безопасно и добавьте проверочный SELECT.",
                "Составьте DELETE для удаления только тестовых строк, предварительно показав их SELECT-запросом.",
            ],
            self.LEVEL_HARD: [
                "Оберните INSERT, UPDATE и DELETE в транзакцию, затем опишите, когда нужен COMMIT, а когда ROLLBACK.",
                "Составьте INSERT INTO ... SELECT для переноса выбранных строк в архивную таблицу.",
            ],
            self.LEVEL_FAILED: [
                "Повторите четыре команды DML и для каждой напишите короткий пример.",
                "Составьте SELECT с WHERE и проверьте, какие строки он возвращает.",
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

    def create_learning_report(self, score_percent, current_difficulty="easy", attempt_number=1):
        level = self.analyze_result(score_percent, current_difficulty)
        grade_points = self.grade_points(score_percent, current_difficulty, attempt_number)
        next_difficulty = self.choose_next_difficulty(current_difficulty, score_percent)
        next_level = self.DIFFICULTY_TO_LEVEL[next_difficulty]
        passed = score_percent >= self.PASS_PERCENT

        if not passed:
            level_result = "уровень не пройден"
            next_step = "Повторить материал и пройти этот же уровень еще раз."
        elif current_difficulty == "hard":
            level_result = "сложный уровень пройден"
            next_step = "Зафиксировать результат или пройти бонус-попытку для повышения балла."
        else:
            level_result = f"уровень «{self.DIFFICULTY_TO_LEVEL[current_difficulty]}» пройден"
            next_step = f"Перейти на уровень «{next_level}»."

        return {
            "score": score_percent,
            "grade_points": grade_points,
            "level": level,
            "level_result": level_result,
            "passed": passed,
            "recommendations": self.generate_recommendation(current_difficulty, score_percent, grade_points),
            "recommendation": "\n".join(self.generate_recommendation(current_difficulty, score_percent, grade_points)),
            "recommended_topics": self.recommend_topics(),
            "next_topic": self.generate_next_topic(),
            "next_step": next_step,
            "practical_task": self.generate_practical_task(),
            "questions_count": self.QUESTION_COUNT,
            "next_difficulty": next_difficulty,
            "next_level": next_level,
            "pass_percent": self.PASS_PERCENT,
            "passing_question_count": self.passing_question_count,
        }
