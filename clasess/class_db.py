import psycopg2


class DBCreating:

    def create_database(self, database_name, params):
        """
        Создание баз данных и таблиц для сохранения данных о работадателях и вакансиях.
        """
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()

        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE employers (
                id_employer INT PRIMARY KEY, 
                company_name VARCHAR(100),
                url TEXT)
                """)

            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE vacancies (
                vacancy_id INT PRIMARY KEY,
                vacancy_name VARCHAR(200) NOT NULL,
                salary_from INT,
                salary_to INT,
                currency VARCHAR(10),
                name_employer VARCHAR(100),
                id_employer INT REFERENCES employers(id_employer),
                url TEXT)
                """)

        conn.close()


class DBManager:

    def __init__(self, db_name, params):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """ Функция для получения списка всех компаний и количество вакансий у каждой компании."""

        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT name_employer, COUNT(name_employer)
                FROM vacancies 
                GROUP BY vacancies.name_employer
                """)

                result = cur.fetchall()

        conn.close()

        return result

    def get_all_vacancies(self):
        """
        Функция для получения списка всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT name_employer, vacancy_name, salary_from, salary_to, url FROM vacancies
                """)

                result = cur.fetchall()

        conn.close()

        return result

    def get_avg_salary(self):
        """
        Функция получает среднюю зарплату по вакансиям.
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT AVG((salary_from+salary_to)/2) FROM vacancies
                """)

                result = cur.fetchall()

        conn.close()

        return result

    def get_vacancies_with_higher_salary(self):
        """
        Функция получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                 SELECT vacancy_name FROM vacancies
                 WHERE ((salary_from+salary_to)/2) > (SELECT AVG((salary_from+salary_to)/2) FROM vacancies)
                """)

                result = cur.fetchall()

        conn.close()

        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Функция получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """

        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                 SELECT * FROM vacancies WHERE vacancy_name LIKE '%{keyword}%'
                """)

                result = cur.fetchall()

        conn.close()

        return result
