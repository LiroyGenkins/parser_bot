import psycopg2


def problem_repr(ans):
    ans = ans[0]
    out_string = "Номер: {}\nНазвание: {}\nКоличество решений: {}\n" \
                 "Темы: {}\nСложность: {}\nСсылка: {}".format(*ans)
    return out_string


def contest_repr(ans, theme, rating):
    out_string = [f"Контест на тему {theme} со сложностью {rating}.\n{'_' * 55}\n"]
    for i, row in enumerate(ans, 1):
        out_string += ["{}. Задача номер: {}\t\"{}\"\n{}\n".format(i, *row)]

    out_string = "".join(out_string)
    return out_string


class Session:

    def open_session(self):
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'
        database = 'parser_bot'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password,
            dbname=database)
        self.cur = self.connection.cursor()

    def close_session(self):
        self.cur.close()
        self.connection.close()

    def put_contest(self, contest):
        contest = [i[0] for i in contest]
        self.cur.execute(f"INSERT INTO contests(theme_name, rating, list_of_problems) "
                         f"values ('математика', 800, array{list(contest)});")
        self.connection.commit()

    def get_contest(self, theme, rating):
        self.open_session()
        self.cur.execute(
            f"SELECT problem_number, problem_name, problem_link FROM problems "
            f"WHERE array['{theme}'] && themes AND rating = {rating} "
            f"AND problem_number NOT IN ("
            f"SELECT unnest(list_of_problems) FROM contests) "
            f"LIMIT 10;")
        contest = self.cur.fetchall()
        if not contest:
            self.cur.execute(
                f"SELECT problem_number, problem_name, problem_link "
                f"FROM problems WHERE array[problem_number] && ("
                f"SELECT list_of_problems FROM contests "
                f"WHERE theme_name='математика' AND rating = 800 LIMIT 1);")
            contest = self.cur.fetchall()
        else:
            self.put_contest(contest)
        self.close_session()
        return contest_repr(contest, theme, rating) if contest else "По Вашему запросу ничего не нашлось."

    def find_problem_by_num(self, number):
        self.open_session()
        self.cur.execute(
            f"SELECT * FROM problems WHERE problem_number='{number}';")
        problem = self.cur.fetchall()
        self.close_session()
        return problem_repr(problem) if problem else "По Вашему запросу ничего не нашлось."

    def find_problem_by_name(self, name):
        self.open_session()
        self.cur.execute(
            f"SELECT * FROM problems WHERE problem_name='{name}';")
        problem = self.cur.fetchall()
        self.close_session()
        return problem_repr(problem) if problem else "По Вашему запросу ничего не нашлось."
