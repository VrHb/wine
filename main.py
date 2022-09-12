import argparse
import collections
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


DEFAULT_FILENAME = 'wines.xlsx'


def get_correct_ending(years: int) -> str:
    number = years % 10
    if number == 1:
        return f"{years} год"
    elif number in range(5, 21):
        return f"{years} лет"
    elif number in range(2, 5):
        return f"{years} года"
    return f"{years} лет"


def group_drinks(drinks: dict) -> dict:
    grouped_drinks = collections.defaultdict(list)
    for drink in drinks:
        grouped_drinks[drink['Категория']].append(drink)
    return grouped_drinks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Описание программы"
    )
    parser.add_argument('file', help="Имя файла или абсолютный путь к файлу")
    args = parser.parse_args()

    company_age = datetime.now().year - 1920       

    try:
        drinks = pandas.read_excel(
            args.file, 
            sheet_name='Лист1',
            keep_default_na=False
        )
    except FileNotFoundError:
        drinks = pandas.read_excel(
            DEFAULT_FILENAME, 
            sheet_name='Лист1',
            keep_default_na=False
        )
    grouped_drinks = group_drinks(drinks.to_dict('record'))
    
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        grouped_drinks=grouped_drinks,
        correct_company_age=get_correct_ending(company_age)      
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()
