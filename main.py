from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from pprint import pprint
import collections

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def get_correct_ending(years: int) -> str:
    number = years % 10
    if number == 1:
        return f"{years} год"
    elif number in range(5, 21):
        return f"{years} лет"
    elif number in range(2, 5):
        return f"{years} года"
    return f"{years} лет"


def sort_drinks(drinks: dict) -> dict:
    sorted_drinks = collections.defaultdict(list)
    for drink in drinks:
        sorted_drinks[drink['Категория']].append(drink)
    return sorted_drinks

start_company_year = datetime(year=1920, month=1, day=1).year
company_age = datetime.now().year - start_company_year       

drinks = pandas.read_excel(
    'wine3.xlsx', 
    sheet_name='Лист1',
    keep_default_na=False
)

sorted_drinks = sort_drinks(drinks.to_dict('record'))
pprint(sorted_drinks)


rendered_page = template.render(
    sorted_drinks=sorted_drinks,
    correct_company_age=get_correct_ending(company_age)      
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
