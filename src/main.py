from clasess.class_db import DBCreating, DBManager
from clasess.class_hh_api import HeadHunterAPI
from utils.config import config


def main():
    """
    Функция для работы с пользователем.
    """
    params = config()
    database_name = "employer_vacansies"

    print("Приветствуем Вас! Данная программа предназначена для получения данных о компаниях и их вакансиях!\n"
          "\nПодождите идет загрузка данных...\n")

    hh = HeadHunterAPI()
    employers, vacancies = hh.get_employers_and_vacancies()

    database = DBCreating(employers, vacancies, database_name, params)
    database.create_database()

    database.save_employers_to_database()
    database.save_vacancies_to_database()

    print(f"Информация по работодателям и их вакансиям получена и сохранена!")

    manager = DBManager(database_name, params)

    while True:
        command = input('\nПожалуйста, выберете один из пунктов и введите его номер:\n'
                        '1: Вывод списка всех компаний и количество вакансий у каждой компании;\n'
                        '2: Вывод списка всех вакансий с указанием названия компании, '
                        'название вакансии, зарплаты (от/до) и ссылки на вакансию;\n'
                        '3: Вывод средней зарплаты по вакансиям;\n'
                        '4: Вывод списка всех вакансий, у которых зарплата выше средней по вакансиям;\n'
                        '5: Вывод списка всех вакансий по Вашему запросу;\n'
                        '6: Выход\n').strip()

        if command.lower() == "1":
            results = manager.get_companies_and_vacancies_count()
            for result in results:
                print(f"{result[0]}: {result[1]}")

        elif command.lower() == "2":
            results = manager.get_all_vacancies()
            for result in results:
                print(f'Компания: {result[0]}, Вакансия: {result[1]}, Зарплата от: {result[2]},'
                      f'Зарплата до: {result[3]}, url: {result[4]}\n')

        elif command.lower() == "3":
            results = manager.get_avg_salary()
            for result in results:
                print(f'Средняя зарплата по всем вакансиям: {result[0]}')

        elif command.lower() == "4":
            results = manager.get_vacancies_with_higher_salary()
            for result in results:
                print(result[0])

        elif command.lower() == "5":
            key_word = input("Введите название вакансии или ключевое слово для поиска\n")
            results = manager.get_vacancies_with_keyword(key_word)
            for result in results:

                print(f'{result[1]}, Зарплата от: {result[2]}, '
                      f'Зарплата до: {result[3]}, Валюта: {result[4]}, '
                      f'Компания: {result[5]}, url: {result[7]}\n'
                      )

        elif command.lower() == "6":
            print("Спасибо, что воспользовались нашей программой.\n"
                  "До свидания!")
            break


if __name__ == '__main__':
    main()
