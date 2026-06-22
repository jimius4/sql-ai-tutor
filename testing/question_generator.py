import random


TOPIC_DML = "dml"

TOPIC_LABELS = {
    TOPIC_DML: "ЯЗЫК DML",
}

DIFFICULTY_LABELS = {
    "easy": "Легкий",
    "medium": "Средний",
    "hard": "Сложный",
}


def make_question(question, answers, correct, explanation):
    return {
        "question": question,
        "answers": answers,
        "correct": correct,
        "explanation": explanation,
    }


QUESTION_BANK = {
    TOPIC_DML: {
        "easy": [
            make_question(
                "Что означает DML в SQL?",
                [
                    "Data Manipulation Language",
                    "Database Migration List",
                    "Data Module Loader",
                    "Digital Markup Language",
                ],
                0,
                "DML означает язык манипулирования данными: команды для чтения и изменения строк.",
            ),
            make_question(
                "Какая команда DML используется для получения данных из таблицы?",
                ["SELECT", "CREATE", "DROP", "ALTER"],
                0,
                "SELECT выбирает данные из одной или нескольких таблиц.",
            ),
            make_question(
                "Какая команда DML добавляет новую строку в таблицу?",
                ["INSERT", "UPDATE", "DELETE", "TRUNCATE"],
                0,
                "INSERT INTO добавляет новые записи в таблицу.",
            ),
            make_question(
                "Для чего в DML-запросах используется WHERE?",
                [
                    "Для ограничения строк по условию",
                    "Для создания новой таблицы",
                    "Для изменения имени базы данных",
                    "Для выдачи прав пользователю",
                ],
                0,
                "WHERE задает условие и помогает работать только с нужными строками.",
            ),
            make_question(
                "Какая команда DML изменяет значения в существующих строках?",
                ["UPDATE", "SELECT", "INSERT", "CREATE"],
                0,
                "UPDATE меняет значения в строках, которые подходят под условие.",
            ),
            make_question(
                "Какая команда DML удаляет строки из таблицы?",
                ["DELETE", "ALTER", "CREATE", "GRANT"],
                0,
                "DELETE удаляет строки, обычно вместе с условием WHERE.",
            ),
            make_question(
                "Что безопаснее сделать перед UPDATE или DELETE?",
                [
                    "Выполнить SELECT с тем же WHERE и проверить строки",
                    "Сразу выполнить запрос без условия",
                    "Удалить таблицу",
                    "Отключить базу данных",
                ],
                0,
                "Проверочный SELECT помогает убедиться, что условие выбрало правильные строки.",
            ),
        ],
        "medium": [
            make_question(
                "Что произойдет при UPDATE table SET status = 'done' без WHERE?",
                [
                    "Изменятся все строки таблицы",
                    "Изменится только первая строка",
                    "Запрос всегда отменится",
                    "Создастся новая таблица",
                ],
                0,
                "Без WHERE команда UPDATE применяется ко всем строкам таблицы.",
            ),
            make_question(
                "Какой запрос корректно добавляет строку в таблицу students?",
                [
                    "INSERT INTO students (name, group_name) VALUES ('Анна', 'ИС-21');",
                    "ADD students VALUES ('Анна', 'ИС-21');",
                    "UPDATE students INSERT ('Анна', 'ИС-21');",
                    "CREATE ROW students ('Анна', 'ИС-21');",
                ],
                0,
                "INSERT INTO указывает таблицу, столбцы и значения новой строки.",
            ),
            make_question(
                "Какой запрос безопасно меняет группу только у студента с id = 5?",
                [
                    "UPDATE students SET group_name = 'ИС-22' WHERE id = 5;",
                    "UPDATE students SET group_name = 'ИС-22';",
                    "DELETE students SET group_name = 'ИС-22' WHERE id = 5;",
                    "ALTER students SET group_name = 'ИС-22' WHERE id = 5;",
                ],
                0,
                "Точное условие WHERE ограничивает изменение одной нужной строкой.",
            ),
            make_question(
                "Какой запрос удаляет только тестовую запись с id = 10?",
                [
                    "DELETE FROM students WHERE id = 10;",
                    "DELETE students id = 10;",
                    "DROP FROM students WHERE id = 10;",
                    "REMOVE TABLE students WHERE id = 10;",
                ],
                0,
                "DELETE FROM удаляет строки из таблицы по заданному условию.",
            ),
            make_question(
                "Какая агрегатная функция считает количество строк?",
                ["COUNT(*)", "SUM(*)", "AVG(*)", "ORDER(*)"],
                0,
                "COUNT(*) возвращает количество строк в результате или группе.",
            ),
            make_question(
                "Для чего используется GROUP BY в DML-запросе SELECT?",
                [
                    "Для группировки строк перед подсчетом агрегатов",
                    "Для удаления строк",
                    "Для добавления столбца",
                    "Для отката транзакции",
                ],
                0,
                "GROUP BY нужен, чтобы считать агрегаты отдельно по группам.",
            ),
            make_question(
                "Какой запрос выбирает товары дороже 100 и сортирует их по цене?",
                [
                    "SELECT * FROM products WHERE price > 100 ORDER BY price;",
                    "SELECT * FROM products ORDER WHERE price > 100;",
                    "UPDATE products WHERE price > 100 ORDER BY price;",
                    "DELETE * FROM products WHERE price > 100 ORDER BY price;",
                ],
                0,
                "WHERE фильтрует строки, а ORDER BY сортирует результат.",
            ),
            make_question(
                "Как проверить результат INSERT?",
                [
                    "Выполнить SELECT с условием, которое находит добавленную строку",
                    "Сразу выполнить DROP TABLE",
                    "Отключить соединение",
                    "Изменить имя базы данных",
                ],
                0,
                "После INSERT результат удобно проверить SELECT-запросом.",
            ),
        ],
        "hard": [
            make_question(
                "Для чего используется INSERT INTO ... SELECT?",
                [
                    "Чтобы вставить строки, выбранные другим SELECT-запросом",
                    "Чтобы удалить строки по условию",
                    "Чтобы создать индекс",
                    "Чтобы переименовать таблицу",
                ],
                0,
                "INSERT INTO ... SELECT переносит или копирует результат выборки в другую таблицу.",
            ),
            make_question(
                "Что делает транзакция при выполнении нескольких DML-команд?",
                [
                    "Позволяет подтвердить все изменения вместе или откатить их",
                    "Всегда ускоряет любой SELECT",
                    "Автоматически создает новую схему",
                    "Запрещает использовать WHERE",
                ],
                0,
                "Транзакция объединяет изменения и дает возможность COMMIT или ROLLBACK.",
            ),
            make_question(
                "Какой оператор откатывает изменения текущей транзакции?",
                ["ROLLBACK", "COMMIT", "INSERT", "GROUP BY"],
                0,
                "ROLLBACK отменяет изменения, сделанные в незавершенной транзакции.",
            ),
            make_question(
                "Какой запрос обновляет цену товаров выбранной категории через подзапрос?",
                [
                    "UPDATE products SET price = price * 1.1 WHERE category_id IN (SELECT id FROM categories WHERE name = 'Tea');",
                    "UPDATE products WHERE SELECT categories;",
                    "INSERT products SET price = price * 1.1;",
                    "DELETE products IN categories;",
                ],
                0,
                "Подзапрос в WHERE помогает выбрать строки на основе данных другой таблицы.",
            ),
            make_question(
                "Как корректно удалить заказы со статусом 'draft', предварительно проверив строки?",
                [
                    "Сначала SELECT * FROM orders WHERE status = 'draft'; затем DELETE FROM orders WHERE status = 'draft';",
                    "Сразу DROP TABLE orders;",
                    "DELETE FROM orders без WHERE;",
                    "UPDATE orders SET status = 'draft';",
                ],
                0,
                "Перед DELETE важно увидеть строки, которые попадут под то же условие.",
            ),
            make_question(
                "Какой вариант лучше для массового изменения важных данных?",
                [
                    "Использовать транзакцию, точное WHERE и предварительный SELECT",
                    "Выполнить UPDATE без проверки",
                    "Удалить ограничения таблицы",
                    "Отключить журналирование запросов",
                ],
                0,
                "Транзакция и проверка условия снижают риск испортить много строк.",
            ),
            make_question(
                "Что делает HAVING в SELECT с GROUP BY?",
                [
                    "Фильтрует группы после агрегирования",
                    "Фильтрует строки до группировки",
                    "Добавляет новую строку",
                    "Удаляет таблицу",
                ],
                0,
                "HAVING применяется к сгруппированным данным и агрегатам.",
            ),
            make_question(
                "Какой запрос найдет группы, где больше 5 студентов?",
                [
                    "SELECT group_name, COUNT(*) FROM students GROUP BY group_name HAVING COUNT(*) > 5;",
                    "SELECT group_name FROM students WHERE COUNT(*) > 5;",
                    "DELETE FROM students GROUP BY group_name;",
                    "INSERT INTO students GROUP BY group_name HAVING COUNT(*) > 5;",
                ],
                0,
                "Условие по COUNT(*) после группировки пишется в HAVING.",
            ),
            make_question(
                "Что означает идемпотентность в контексте учебных DML-скриптов?",
                [
                    "Повторный запуск не должен портить данные или создавать неожиданные дубли",
                    "Запрос обязан работать только без WHERE",
                    "Запрос должен удалять все строки",
                    "SELECT должен менять данные",
                ],
                0,
                "Для учебных скриптов полезно писать условия так, чтобы повторный запуск был безопасным.",
            ),
            make_question(
                "Какой подход помогает избежать дублей при INSERT тестовой строки?",
                [
                    "Проверить существование строки условием NOT EXISTS или уникальным ключом",
                    "Выполнять INSERT много раз подряд",
                    "Удалить первичный ключ",
                    "Использовать DELETE без WHERE",
                ],
                0,
                "Проверка существования и ограничения уникальности защищают от повторных вставок.",
            ),
        ],
    },
}


def generate_test(topic, level, question_count=None):
    topic_questions = QUESTION_BANK.get(topic) or QUESTION_BANK[TOPIC_DML]
    questions = topic_questions.get(level, topic_questions["easy"])

    count = question_count or len(questions)
    return random.sample(questions, min(count, len(questions)))


def check_answers(user_answers, questions):
    correct_count = 0
    details = []

    for index, question in enumerate(questions):
        field_name = f"question_{index}"
        raw_answer = user_answers.get(field_name)
        selected_index = int(raw_answer) if raw_answer is not None and raw_answer.isdigit() else None
        if selected_index is not None and not 0 <= selected_index < len(question["answers"]):
            selected_index = None

        correct_index = question["correct"]
        is_correct = selected_index == correct_index

        if is_correct:
            correct_count += 1

        details.append(
            {
                "number": index + 1,
                "question": question["question"],
                "answers": question["answers"],
                "selected_index": selected_index,
                "selected_answer": question["answers"][selected_index] if selected_index is not None else "Ответ не выбран",
                "correct_index": correct_index,
                "correct_answer": question["answers"][correct_index],
                "is_correct": is_correct,
                "explanation": question.get("explanation", ""),
            }
        )

    total = len(questions)
    incorrect_count = total - correct_count
    score_percent = round((correct_count / total) * 100, 1) if total else 0

    return {
        "total": total,
        "correct_count": correct_count,
        "incorrect_count": incorrect_count,
        "score_percent": score_percent,
        "score_percent_width": str(score_percent),
        "details": details,
    }
