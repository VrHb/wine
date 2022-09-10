from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

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


start_company_year = datetime(year=1920, month=1, day=1).year
company_age = datetime.now().year - start_company_year       

wines = pandas.read_excel('wine.xlsx').to_dict(orient='record')

rendered_page = template.render(
    wines=wines,
    correct_company_age=get_correct_ending(company_age)      
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
