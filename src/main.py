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
    hh.get_employers_and_vacancies()

    database = DBCreating()
    database.create_database(database_name, params)

    hh.save_employers_to_database(database_name, params)
    hh.save_vacancies_to_database(database_name, params)

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
            print(manager.get_companies_and_vacancies_count())

        elif command.lower() == "2":
            print(manager.get_all_vacancies())

        elif command.lower() == "3":
            print(manager.get_avg_salary())

        elif command.lower() == "4":
            print(manager.get_vacancies_with_higher_salary())

        elif command.lower() == "5":
            key_word = input("Введите название вакансии или ключевое слово для поиска\n")
            print(manager.get_vacancies_with_keyword(key_word))

        elif command.lower() == "6":
            print("Спасибо, что воспользовались нашей программой.\n"
                  "До свидания!")
            break


if __name__ == '__main__':
    main()
