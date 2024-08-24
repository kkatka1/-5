import requests
from typing import Any, List, Dict

# Список компаний
companies_data = {
    '1': 78638,
    '2': 1740,
    '3': 2180,
    '4': 87021,
    '5': 3530,
    '6': 1455,
    '7': 776314,
    '8': 3529,
    '9': 4181,
    '10': 80,
}

class HeadHunterRuAPI:
    """
    Класс для взаимодействия с API HH.ru и получения данных о компаниях и вакансиях.
    """
    @staticmethod
    def fetch_company_data() -> List[Dict[str, Any]]:
        """
        Получает данные о компаниях с HH.ru.
        :return: список словарей с информацией по компаниям.
        """
        data_company = []
        base_url = 'https://api.hh.ru/employers/'

        for company_name, company_id in companies_data.items():
            response = requests.get(f'{base_url}{company_id}').json()
            data_company.append(response)
        return data_company

    @staticmethod
    def fetch_vacancies_data() -> List[Dict[str, Any]]:
        """
        Получает по 10 вакансий для каждой компании.
        :return: список словарей с вакансиями по компаниям.
        """
        data_vacancy = []
        base_url = 'https://api.hh.ru/vacancies?employer_id='

        for company_name, company_id in companies_data.items():
            response = requests.get(f'{base_url}{company_id}', params={'page': 0, 'per_page': 100}).json()['items']
            data_vacancy.append(response)
        return data_vacancy