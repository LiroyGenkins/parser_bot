import psycopg2

# Формирование красивого вывода для задачи
def problem_repr(ans):
    ans = ans[0]
    out_string = "Номер: {}\nНазвание: {}\nКоличество решений: {}\n" \
                 "Темы: {}\nСложность: {}\nСсылка: {}".format(*ans)
    return out_string

# Формирование красивого вывода для таблицы контеста
def contest_repr(ans, theme, rating):
    out_string = [f"Контест на тему {theme} со сложностью {rating}.\n{'_' * 55}\n"]
    for i, row in enumerate(ans, 1):
        out_string += ["{}. Задача номер: {}\t\"{}\"\n{}\n".format(i, *row)]

    out_string = "".join(out_string)
    return out_string


class Session:
    """
    Класс управления соединением с БД и поисковых запросов к ней
    """
    def __init__(self, hostname='localhost', username='postgres',
                 password='postgres', database='parser_bot'):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database

    # Создание подключения к БД
    def open_session(self):
        self.connection = psycopg2.connect(
            host=self.hostname, user=self.username, password=self.password,
            dbname=self.database)
        self.cur = self.connection.cursor()
        self.create_tables()

    # Создание таблиц
    def create_tables(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS problems("
                         "problem_number TEXT PRIMARY KEY, "
                         "problem_name TEXT, "
                         "solves INT, "
                         "themes TEXT[],"
                         "rating INT,"
                         "problem_link TEXT NOT NULL);")
        self.cur.execute("CREATE TABLE IF NOT EXISTS contests("
                         "contest_id SERIAL PRIMARY KEY,"
                         "theme_name TEXT,"
                         "rating INT,"
                         "list_of_problems TEXT[10]);")
        self.connection.commit()

    # Закрытие подключения
    def close_session(self):
        self.cur.close()
        self.connection.close()

    # Запись сформированного контеста в БД
    def put_contest(self, contest, theme, rating):
        contest = [i[0] for i in contest]
        self.cur.execute(f"INSERT INTO contests(theme_name, rating, list_of_problems) "
                         f"values ('{theme}', {rating}, array{list(contest)});")
        self.connection.commit()

    # Формирование контеста
    def get_contest(self, theme, rating):
        self.open_session()
        self.cur.execute(
            f"SELECT problem_number, problem_name, problem_link FROM problems "
            f"WHERE array['{theme}'] && themes AND rating = {rating} "
            f"AND problem_number NOT IN ("
            f"SELECT unnest(list_of_problems) FROM contests) "
            f"LIMIT 10;")
        contest = self.cur.fetchall()

        # Если новые задачи по этим параметрам кончились, то берем существующий контест
        if not contest:
            self.cur.execute(
                f"SELECT problem_number, problem_name, problem_link "
                f"FROM problems WHERE array[problem_number] && ("
                f"SELECT list_of_problems FROM contests "
                f"WHERE theme_name='{theme}' AND rating = {rating} LIMIT 1);")
            contest = self.cur.fetchall()
        else:
            self.put_contest(contest, theme, rating)
        self.close_session()
        return contest_repr(contest, theme, rating) if contest else "По Вашему запросу ничего не нашлось."

    # Поиск задачи по номеру
    def find_problem_by_num(self, number):
        self.open_session()
        self.cur.execute(
            f"SELECT * FROM problems WHERE problem_number='{number}';")
        problem = self.cur.fetchall()
        self.close_session()
        return problem_repr(problem) if problem else "По Вашему запросу ничего не нашлось."

    # Поиск задачи по имени
    def find_problem_by_name(self, name):
        self.open_session()
        self.cur.execute(
            f"SELECT * FROM problems WHERE problem_name='{name}';")
        problem = self.cur.fetchall()
        self.close_session()
        return problem_repr(problem) if problem else "По Вашему запросу ничего не нашлось."
