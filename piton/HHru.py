import requests
from bs4 import BeautifulSoup
import json

# Функция для парсинга вакансий с заданными параметрами
def parse_vacancies():
    base_url = "https://hh.ru/search/vacancy"
    params = {
        "text": "Python",
        "area": [1, 2],  # Москва - 1, Санкт-Петербург - 2
        "page": 0  # Начальная страница
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    vacancies = []  # Список для хранения информации о вакансиях

    while True:
        # Отправляем запрос к странице с вакансиями
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {params['page']}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Находим все блоки вакансий на странице
        vacancy_items = soup.find_all("div", class_="vacancy-serp-item")
        if not vacancy_items:
            break  # Если вакансий больше нет, выходим из цикла

        for item in vacancy_items:
            # Извлечение данных о вакансии
            title_tag = item.find("a", class_="bloko-link")
            title = title_tag.text.strip() if title_tag else ""
            link = title_tag["href"] if title_tag else ""

            description = item.find("div", class_="g-user-content").text.lower() if item.find("div", class_="g-user-content") else ""

            if "django" in description and "flask" in description:
                # Извлечение зарплаты
                salary_tag = item.find("span", class_="bloko-header-section-3")
                salary = salary_tag.text.strip() if salary_tag else "Не указана"

                # Извлечение информации о компании
                company_tag = item.find("a", class_="bloko-link_secondary")
                company = company_tag.text.strip() if company_tag else "Не указана"

                # Извлечение информации о городе
                city_tag = item.find("div", class_="vacancy-serp-item__meta-info")
                city = city_tag.text.strip() if city_tag else "Не указан"

                # Сохранение данных о вакансии
                vacancies.append({
                    "title": title,
                    "link": link,
                    "salary": salary,
                    "company": company,
                    "city": city
                })

        # Переход к следующей странице
        params["page"] += 1

    # Запись вакансий в JSON-файл
    with open("vacancies.json", "w", encoding="utf-8") as file:
        json.dump(vacancies, file, ensure_ascii=False, indent=4)

    print(f"Сохранено {len(vacancies)} вакансий в файл vacancies.json")

# Запуск функции
if __name__ == "__main__":
    parse_vacancies()
