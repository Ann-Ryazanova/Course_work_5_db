import psycopg2


class DBCreating:

    def __init__(self, employers, vacancies, db_name, params):
        self.employers = employers
        self.vacancies = vacancies
        self.db_name = db_name
        self.params = params

    def create_database(self):
        """
        Создание и сохранение баз данных и таблиц о работадателях и вакансиях.
        """
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        cur.execute(f"CREATE DATABASE {self.db_name}")

        conn.close()

        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                id_employer INT PRIMARY KEY, 
                company_name VARCHAR(100),
                url TEXT)
                """)

            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
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

    def save_employers_to_database(self):
        """ Функция для сохранения данных о компаниях в таблицу БД. """

        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                for employer in self.employers:
                    cur.execute(
                        """
                        INSERT INTO employers (id_employer, company_name, url) 
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id_employer) DO NOTHING
                        """,
                        (employer['id_company'], employer['name_company'], employer['url']))

        conn.close()

    def save_vacancies_to_database(self):
        """ Функция для сохранения данных о вакансиях компаний в таблицу БД """

        with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                for vacancy in self.vacancies:
                    cur.execute("""
                       INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to,
                       currency, name_employer, id_employer, url) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                       ON CONFLICT (vacancy_id) DO NOTHING
                       """,
                                (vacancy['id_vacancy'], vacancy['title'], vacancy['salary_min'],
                                 vacancy['salary_max'], vacancy['currency'], vacancy['employer'],
                                 vacancy['id_employer'], vacancy['url']))

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
