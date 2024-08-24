from src.api_hh.api_hh import HeadHunterRuAPI
from src.database_postgresql.database_postgresql import DatabaseManager
from src.db_manager.db_manager import DBManager
import config


def main():
    # Чтение конфигурации
    db_params = config.config()
    db_name = 'hh_database'

    # Получение данных по API
    hh_api = HeadHunterRuAPI()
    companies = hh_api.fetch_company_data()
    vacancies = hh_api.fetch_vacancies_data()

    # Создание базы данных и таблиц
    DatabaseManager.initialize_database(db_name, db_params)

    # Внесение данных в таблицы

    DatabaseManager.insert_company_data(companies, db_name, db_params)
    DatabaseManager.insert_vacancy_data(vacancies, db_name, db_params)

    # Выполнение запросов к базе данных
    db_manager = DBManager(db_name, db_params)
    # db_manager.init(db_name, db_params)

    print("Компании и количество вакансий:")
    for company in db_manager.get_companies_and_vacancies_count():
        print(company)

    print("\nВсе вакансии:")
    for vacancy in db_manager.get_all_vacancies():
        print(vacancy)

    print("\nСредняя зарплата по вакансиям:")
    avg_salary = db_manager.get_avg_salary()
    if avg_salary is not None:
        print(f'{avg_salary:.2f}')
    else:
        print(f'Средняя зарплата не найдена')

    print("\nВакансии с зарплатой выше средней:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(vacancy)

    keyword = 'Python'
    print(f"\nВакансии по ключевому слову '{keyword}':")
    for vacancy in db_manager.get_vacancies_with_keyword(keyword):
        print(vacancy)


if __name__ == '__main__':
    main()