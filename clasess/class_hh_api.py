import psycopg2
import requests


class HeadHunterAPI:
    """ Класс для получения и сохранения данных о работодателях и их вакансиях. """
    def __init__(self):
        self.employers_id = ["4934", "3529"]
        self.__header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/110.0.0.0 YaBrowser/23.3.3.721 Yowser/2.5 Safari/537.36"
        }
        self.__params = {"page": 0,
                         "per_page": 100,
                         "only_with_salary": True}

        self.employers = []
        self.vacancies = []

    def get_request_employers(self, employer_id):
        """ Функция для запроса данных о компаниях по id через API с HeadHunter. """

        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url,
                                params=self.__params,
                                headers=self.__header)

        if response.status_code != 200:
            raise f"Request failed with status code: {response.status_code}"

        return response.json()

    def get_request_vacancies(self, employer_id):
        """ Функция для запроса данных вакансий компаний по id работодателя через API с HeadHunter. """

        url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        response = requests.get(url,
                                params=self.__params,
                                headers=self.__header)

        if response.status_code != 200:
            raise f"Request failed with status code: {response.status_code}"

        return response.json()['items']

    def get_employers_and_vacancies(self):
        """Функция позволяющий положить данные о вакансиях и работодателях в список, для дальнейшего сохранения в БД"""

        for emp in self.employers_id:
            employer = self.get_request_employers(emp)
            self.employers.append({'id_company': employer['id'], 'name_company': employer['name'],
                                   'url': employer['alternate_url']})

            for self.__params['page'] in range(20):
                values = self.get_request_vacancies(emp)
                for val in values:
                    if val['salary']['currency'].lower() == 'rur':
                        salary_min, salary_max = self.get_salary(val['salary'])
                        self.vacancies.append({"id_vacancy": val['id'],
                                               "title": val['name'],
                                               "salary_min": salary_min,
                                               "salary_max": salary_max,
                                               "currency": val['salary']['currency'],
                                               "employer": val['employer']['name'],
                                               "id_employer": val['employer']['id'],
                                               "url": val['alternate_url'],
                                               })

                    else:
                        continue

        return self.employers, self.vacancies

    @staticmethod
    def get_salary(salary):
        """ Функция заполняет salary['to'], salary['from'], если они None для базы данных """
        formatted_salary = [None, None]
        if salary['from'] is None:
            formatted_salary[0] = salary['to']
        else:
            formatted_salary[0] = salary['from']
        if salary['to'] is None:
            formatted_salary[1] = salary['from']
        else:
            formatted_salary[1] = salary['to']

        return formatted_salary

    def save_employers_to_database(self, db_name, params):
        """ Функция для сохранения данных о компаниях в таблицу БД. """

        with psycopg2.connect(dbname=db_name, **params) as conn:
            with conn.cursor() as cur:
                for employer in self.employers:
                    cur.execute(
                        """
                        INSERT INTO employers (id_employer, company_name, url) 
                        VALUES (%s, %s, %s)
                        """,
                        (employer['id_company'], employer['name_company'], employer['url']))

        conn.close()

    def save_vacancies_to_database(self, db_name, params):
        """ Функция для сохранения данных о вакансиях компаний в таблицу БД """

        with psycopg2.connect(dbname=db_name, **params) as conn:
            with conn.cursor() as cur:
                for vacancy in self.vacancies:
                    cur.execute("""
                    INSERT INTO vacancies (vacancy_id, vacancy_name, salary_from, salary_to,
                    currency, name_employer, id_employer, url) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                                (vacancy['id_vacancy'], vacancy['title'], vacancy['salary_min'],
                                 vacancy['salary_max'], vacancy['currency'], vacancy['employer'],
                                 vacancy['id_employer'], vacancy['url']))

        conn.close()
