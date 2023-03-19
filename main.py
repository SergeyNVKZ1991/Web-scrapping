import requests
from pprint import pprint
from bs4 import BeautifulSoup
# from fake_headers import Headers
import json

# def get_headers():
#     return Headers(browser='chrome', os='win').generate()

HOST = 'https://hh.ru/search/vacancy?text=python&area=1&area=2'
headers = {'Accept': '*/*', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36', 'Accept-Language': 'en-US;q=0.5,en;q=0.3', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1'}
html = requests.get(HOST, headers=headers).text

soup = BeautifulSoup(html, features='lxml')
all_vacancies = soup.find(id='a11y-main-content') # находим список вакансий
vacancy = all_vacancies.find_all(class_='serp-item') # выделяем класс который описывает каждую вакансию в списке

description_list = [] # создаем пустой список
for item in vacancy: # создаем цикл для перебора каждай вакансии
    description_vacancy = item.find(class_='vacancy-serp-item__layout') # находим вакансию
    description = description_vacancy.find('a', class_='serp-item__title').text # выделяем в этой вакансии текст заголовка
    if 'Django' in description or 'Flask' in description: #если в заголовке имеется текст 'Django' или 'Flask'
        description_list.append(item) # добавляем вакансию в список

vacancy_list = [] # создаем пустой список для записи уже отфильтрованных вакансий
for word in description_list: #создаем цикл для перебора списка вакансий
    title = word.find('a', class_='serp-item__title').text #объявляем переменную в которую помещааем заголовок вакансии
    link_tag = word.find('a', class_='serp-item__title')
    link = link_tag['href'] #объявляем переменную в которую помещаем ссылку
    try: # создаем исключение
        salary_tag = word.find('span', class_='bloko-header-section-3')
        salary = salary_tag.text
    except Exception: # если зарплата не указана срабатывает исключение
        salary = 'Не указана'
    company_tag = word.find('a', class_='bloko-link bloko-link_kind-tertiary') # создаем переменную в которую вкладываем информацию о компании
    company = company_tag.text # переводим в текстовый формат
    city_tag = word.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'}) # создаем переменную в которую вкладываем информацию о городе
    city = city_tag.text # переводим в текстовый формат

    vacancy_list.append({

        'Название': title,
        'Зарплата': salary,
        'Компания': company,
        'Город': city,
        'Ссылка': link

    })  # создаем в списке словарь, в кторый вкладываем нужные переменные

with open('vacancy.json', 'w', encoding='utf=8') as f: # записываем словарь в файл .json
    json.dump(vacancy_list, f, ensure_ascii=False)


if __name__ == '__main__':
    pprint(vacancy_list)
    pass