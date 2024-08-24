import psycopg2

class DBManager:
    """Класс для работы с БД PostgreSQL."""

    def __init__(self, db_name:str, params:dict):
        if 'database' in params:
            params.pop('database')

        self.conn = psycopg2.connect(database=db_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        self.cur.execute("""
           SELECT company.company_name, COUNT(vacancy.company_id)
           FROM company
           JOIN vacancy USING (company_id)
           GROUP BY company.company_name
           ORDER BY COUNT DESC
           """)

        return self.cur.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        self.cur.execute("""
           SELECT company.company_name, vacancy.vacancy_name, vacancy.salary, vacancy.vacancy_url
           FROM vacancy
           JOIN company USING (company_id)
           ORDER BY salary DESC""")
        return self.cur.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        self.cur.execute("""
           SELECT avg(salary) FROM vacancy""")
        avg_salary = self.cur.fetchone()[0]
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        self.cur.execute("""
           SELECT vacancy_name, salary, vacancy_url
           FROM vacancy
           WHERE salary > (SELECT AVG(salary) FROM vacancy)
           ORDER BY salary DESC
           """)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword:str):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        self.cur.execute("""
           SELECT * FROM vacancy
           WHERE LOWER(vacancy_name) LIKE %s
           """, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()