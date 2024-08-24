import psycopg2
from typing import Any, List, Dict

class DatabaseManager:
    """
    Класс для работы с базой данных PostgreSQL.
    """

    @staticmethod
    def initialize_database(db_name: str, params: dict) -> None:
        """
        Создает базу данных и таблицы в ней.
        """
        params.pop('database', None)

        conn = psycopg2.connect(database=db_name, **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS vacancy')
        cur.execute('DROP TABLE IF EXISTS company')

        cur.execute("""
            CREATE TABLE company (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                company_area VARCHAR(255) NOT NULL,
                url TEXT,
                open_vacancies INTEGER
            )
        """)
        cur.execute("""
            CREATE TABLE vacancy (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR(255),
                vacancy_area VARCHAR(255),
                salary INTEGER,
                company_id INT REFERENCES company(company_id),
                vacancy_url VARCHAR(255)
            )
        """)

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def insert_company_data(company_data: List[Dict[str, Any]], db_name: str, params: dict) -> None:
        """
        Заполняет таблицу компаний в БД.
        """
        conn = psycopg2.connect(database=db_name, **params)
        cur = conn.cursor()

        for company in company_data:
            if 'id' not in company or 'name' not in company or 'area' not in company or 'name' not in company['area']:
                print(f"Ощибка: в данных компании отсутсвуют ключи. Данные компании:{company}")
                continue

            cur.execute('SELECT 1 FROM company WHERE  company_id = %s', (company['id'],))
            if cur.fetchone():
                print(f'компания с ID {company["id"]}уже существует в бд')
                continue

            cur.execute("""
                INSERT INTO company (company_id, company_name, company_area, url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                """,
                        (company['id'], company['name'], company['area']['name'], company['alternate_url'], company['open_vacancies']))

        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def insert_vacancy_data(vacancy_data: List[Dict[str, Any]], db_name: str, params: dict) -> None:
        """
        Метод для заполнения таблицы вакансий в БД
        """
        conn = psycopg2.connect(database=db_name, **params)
        cur = conn.cursor()

        for vacancies in vacancy_data:
            for vacancy in vacancies:
                cur.execute('SELECT 1 FROM vacancy WHERE  vacancy_id = %s', (vacancy['id'],))
                if cur.fetchone():
                    print(f'кВакансия с ID {vacancy["id"]}уже существует в бд')
                    continue

                salary = vacancy.get('salary')
                salary_value = 0 if salary is None else (salary.get('from') or salary.get('to') or 0)

                cur.execute("""
                    INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, company_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                            (vacancy['id'], vacancy['name'], vacancy['area']['name'], salary_value,
                             vacancy['employer']['id'], vacancy['alternate_url']))


        conn.commit()
        cur.close()
        conn.close()