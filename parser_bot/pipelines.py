# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2


class ProblemPipeline(object):
    """
    Pipline для сохранения собранной информации о задачах в БД PostgreSQL
    """

    # Define function to configure the connection to the database & connect to it
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'postgres'
        database = 'parser_bot'
        self.connection = psycopg2.connect(
            host=hostname, user=username, password=password,
            dbname=database)
        self.cur = self.connection.cursor()

    # Define function to disconnect from database
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    # Define function to process each scraped item and insert it into PostgreSQL table
    def process_item(self, item, spider):
        try:
            # Execute SQL command on database to insert data in table
            self.cur.execute(
                "insert into problems(problem_number, problem_name, solves, themes, rating, problem_link) "
                "values(%s,%s,%s,%s,%s,%s) "
                "ON CONFLICT (problem_number) DO NOTHING;"
                "UPDATE problems "
                "SET problem_name=%s, solves=%s, themes=%s, rating=%s, problem_link=%s"
                "WHERE problem_number=%s;",
                (item['problem_number'], item['problem_name'], item['solves'],
                 item['themes'], item['rating'], item['problem_link'],
                 item['problem_name'], item['solves'], item['themes'],
                 item['rating'], item['problem_link'], item['problem_number']))
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item
