import random


TOPIC_DML = "dml"
ANSWER_LETTERS = ["А", "Б", "В", "Г"]

TOPIC_LABELS = {
    TOPIC_DML: "ЯЗЫК DML",
}

DIFFICULTY_LABELS = {
    "easy": "Легкий",
    "medium": "Средний",
    "hard": "Сложный",
}


def make_question(question, answers, correct, explanation=""):
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
                ["Data Manipulation Language", "Database Migration List", "Data Module Loader", "Digital Markup Language"],
                0,
            ),
            make_question(
                "Какая команда DML используется для получения данных из таблицы?",
                ["SELECT", "CREATE", "DROP", "ALTER"],
                0,
            ),
            make_question(
                "Какая команда DML добавляет новую строку в таблицу?",
                ["INSERT", "UPDATE", "DELETE", "TRUNCATE"],
                0,
            ),
            make_question(
                "Какая команда DML изменяет значения в существующих строках?",
                ["UPDATE", "SELECT", "INSERT", "CREATE"],
                0,
            ),
            make_question(
                "Какая команда DML удаляет строки из таблицы?",
                ["DELETE", "ALTER", "CREATE", "GRANT"],
                0,
            ),
            make_question(
                "Для чего в DML-запросах используется WHERE?",
                ["Для ограничения строк по условию", "Для создания таблицы", "Для выдачи прав", "Для удаления базы данных"],
                0,
            ),
            make_question(
                "Какая часть запроса SELECT указывает таблицу-источник?",
                ["FROM", "VALUES", "SET", "COMMIT"],
                0,
            ),
            make_question(
                "Что делает ORDER BY в SELECT-запросе?",
                ["Сортирует результат", "Удаляет строки", "Добавляет строки", "Откатывает транзакцию"],
                0,
            ),
            make_question(
                "Что делает LIMIT в SELECT-запросе?",
                ["Ограничивает количество строк результата", "Создает ограничение таблицы", "Удаляет лишние столбцы", "Меняет тип данных"],
                0,
            ),
            make_question(
                "Какая запись корректно проверяет отсутствие значения?",
                ["IS NULL", "= NULL", "LIKE NULL", "IN NULL"],
                0,
            ),
            make_question(
                "Какая команда фиксирует изменения транзакции?",
                ["COMMIT", "ROLLBACK", "SELECT", "WHERE"],
                0,
            ),
            make_question(
                "Какая команда отменяет изменения незавершенной транзакции?",
                ["ROLLBACK", "COMMIT", "INSERT", "ORDER BY"],
                0,
            ),
            make_question(
                "Что безопаснее сделать перед UPDATE или DELETE?",
                ["Выполнить SELECT с тем же WHERE", "Сразу выполнить запрос без WHERE", "Удалить таблицу", "Отключить базу"],
                0,
            ),
            make_question(
                "Какая команда DML работает с уже существующими строками, а не со структурой таблицы?",
                ["UPDATE", "ALTER", "CREATE", "DROP"],
                0,
            ),
            make_question(
                "Какая команда НЕ относится к DML?",
                ["CREATE TABLE", "SELECT", "INSERT", "DELETE"],
                0,
            ),
        ],
        "medium": [
            make_question(
                "Что произойдет при UPDATE students SET group_name = 'ИС-22' без WHERE?",
                ["Изменятся все строки таблицы", "Изменится только первая строка", "Запрос создаст новую таблицу", "Запрос станет SELECT-запросом"],
                0,
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
            ),
            make_question(
                "Какой запрос удаляет только тестовую запись с id = 10?",
                ["DELETE FROM students WHERE id = 10;", "DELETE students id = 10;", "DROP FROM students WHERE id = 10;", "REMOVE TABLE students WHERE id = 10;"],
                0,
            ),
            make_question(
                "Какая агрегатная функция считает количество строк?",
                ["COUNT(*)", "SUM(*)", "AVG(*)", "ORDER(*)"],
                0,
            ),
            make_question(
                "Для чего используется GROUP BY в SELECT?",
                ["Для группировки строк перед подсчетом агрегатов", "Для удаления строк", "Для добавления столбца", "Для отката транзакции"],
                0,
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
            ),
            make_question(
                "Как проверить результат INSERT?",
                ["Выполнить SELECT с условием, которое находит добавленную строку", "Сразу выполнить DROP TABLE", "Отключить соединение", "Изменить имя базы"],
                0,
            ),
            make_question(
                "Где нужно писать условие по агрегатной функции COUNT(*)?",
                ["HAVING", "WHERE", "VALUES", "SET"],
                0,
            ),
            make_question(
                "Какой запрос найдет группы, где больше пяти студентов?",
                [
                    "SELECT group_name, COUNT(*) FROM students GROUP BY group_name HAVING COUNT(*) > 5;",
                    "SELECT group_name FROM students WHERE COUNT(*) > 5;",
                    "DELETE FROM students GROUP BY group_name;",
                    "INSERT INTO students GROUP BY group_name HAVING COUNT(*) > 5;",
                ],
                0,
            ),
            make_question(
                "В каком порядке безопаснее выполнять удаление строк?",
                ["SELECT для проверки, затем DELETE с тем же WHERE", "DELETE без проверки, затем SELECT", "DROP TABLE, затем SELECT", "COMMIT, затем WHERE"],
                0,
            ),
            make_question(
                "Что делает DISTINCT в SELECT?",
                ["Убирает повторяющиеся значения из результата", "Удаляет строки из таблицы", "Добавляет новую строку", "Откатывает транзакцию"],
                0,
            ),
            make_question(
                "Какой оператор проверяет попадание значения в список?",
                ["IN", "BETWEEN", "LIKE", "IS NULL"],
                0,
            ),
            make_question(
                "Какой оператор проверяет диапазон значений?",
                ["BETWEEN", "IN", "LIKE", "IS NOT NULL"],
                0,
            ),
            make_question(
                "В каком фрагменте UPDATE правильно указано новое значение столбца?",
                ["SET status = 'done'", "VALUES status = 'done'", "FROM status = 'done'", "ORDER status = 'done'"],
                0,
            ),
        ],
        "hard": [
            make_question(
                "Для чего используется INSERT INTO ... SELECT?",
                ["Чтобы вставить строки, выбранные другим SELECT-запросом", "Чтобы удалить строки по условию", "Чтобы создать индекс", "Чтобы переименовать таблицу"],
                0,
            ),
            make_question(
                "Что делает транзакция при выполнении нескольких DML-команд?",
                ["Позволяет подтвердить все изменения вместе или откатить их", "Всегда ускоряет любой SELECT", "Создает новую схему", "Запрещает WHERE"],
                0,
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
            ),
            make_question(
                "Какой вариант лучше для массового изменения важных данных?",
                ["Использовать транзакцию, точное WHERE и предварительный SELECT", "Выполнить UPDATE без проверки", "Удалить ограничения таблицы", "Отключить журналирование"],
                0,
            ),
            make_question(
                "Что делает HAVING в SELECT с GROUP BY?",
                ["Фильтрует группы после агрегирования", "Фильтрует строки до группировки", "Добавляет новую строку", "Удаляет таблицу"],
                0,
            ),
            make_question(
                "Что означает идемпотентность учебного DML-скрипта?",
                ["Повторный запуск не портит данные и не создает неожиданные дубли", "Запрос работает только без WHERE", "Запрос удаляет все строки", "SELECT меняет данные"],
                0,
            ),
            make_question(
                "Какой подход помогает избежать дублей при INSERT тестовой строки?",
                ["Проверить существование строки через NOT EXISTS или уникальный ключ", "Выполнять INSERT много раз подряд", "Удалить первичный ключ", "Использовать DELETE без WHERE"],
                0,
            ),
            make_question(
                "Какой запрос переносит активных студентов в архивную таблицу?",
                [
                    "INSERT INTO archive_students SELECT * FROM students WHERE active = true;",
                    "UPDATE archive_students SELECT active FROM students;",
                    "DELETE INTO archive_students FROM students;",
                    "CREATE INTO archive_students WHERE active = true;",
                ],
                0,
            ),
            make_question(
                "Как найти ошибку в DELETE FROM orders; для удаления черновиков?",
                ["Не указано условие WHERE status = 'draft'", "Нельзя удалять из таблицы orders", "Нужно заменить DELETE на SELECT", "Нужно добавить ORDER BY"],
                0,
            ),
            make_question(
                "Какой фрагмент защищает UPDATE от изменения лишних строк?",
                ["WHERE id IN (SELECT student_id FROM exam_results WHERE score < 61)", "ORDER BY id", "LIMIT без условия", "SELECT *"],
                0,
            ),
            make_question(
                "Что лучше сделать после ROLLBACK?",
                ["Проверить данные SELECT-запросом и исправить условие", "Повторить тот же ошибочный UPDATE", "Удалить таблицу", "Отключить WHERE"],
                0,
            ),
            make_question(
                "Какой сценарий лучше всего подходит для транзакции?",
                ["Несколько связанных INSERT/UPDATE/DELETE, которые должны выполниться вместе", "Один SELECT без условий", "Просмотр структуры таблицы", "Смена темы интерфейса"],
                0,
            ),
            make_question(
                "Как применить DML с подзапросом для анализа результата?",
                ["Сначала проверить подзапрос отдельно, затем использовать его в WHERE", "Сразу выполнить DELETE без просмотра", "Заменить подзапрос на DROP", "Не использовать SELECT"],
                0,
            ),
            make_question(
                "Что нужно сделать перед COMMIT после массового UPDATE?",
                ["Проверить измененные строки SELECT-запросом внутри транзакции", "Сразу закрыть подключение", "Удалить журнал запросов", "Выполнить DROP DATABASE"],
                0,
            ),
        ],
    },
}


def _prepare_question(question, target_correct_index):
    correct_answer = question["answers"][question["correct"]]
    wrong_answers = [
        answer
        for index, answer in enumerate(question["answers"])
        if index != question["correct"]
    ]
    random.shuffle(wrong_answers)
    answers = wrong_answers[:]
    answers.insert(target_correct_index, correct_answer)

    prepared = {
        **question,
        "answers": answers,
        "correct": target_correct_index,
    }
    prepared["options"] = [
        {
            "index": index,
            "letter": ANSWER_LETTERS[index],
            "text": answer,
        }
        for index, answer in enumerate(answers)
    ]
    return prepared


def generate_test(topic, level, question_count=15):
    topic_questions = QUESTION_BANK.get(topic) or QUESTION_BANK[TOPIC_DML]
    questions = topic_questions.get(level, topic_questions["easy"])
    count = min(question_count, len(questions))
    selected_questions = random.sample(questions, count)

    target_indexes = [index % len(ANSWER_LETTERS) for index in range(count)]
    random.shuffle(target_indexes)

    return [
        _prepare_question(question, target_indexes[index])
        for index, question in enumerate(selected_questions)
    ]


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
                "selected_index": selected_index,
                "is_correct": is_correct,
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
