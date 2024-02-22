
from jinja2 import Environment, FileSystemLoader
import json


def main(data):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("template.html")

    EUR = data[0]
    USD = data[1]

    data_EUR = json.loads(EUR)
    rates_EUR = sorted(data_EUR["rates"],
                       key=lambda x: x["effectiveDate"], reverse=True)

    data_USD = json.loads(USD)
    rates_USD = sorted(data_USD["rates"],
                       key=lambda x: x["effectiveDate"], reverse=True)
    output = template.render(rates_EUR=rates_EUR, rates_USD=rates_USD)

    with open("index.html", "w", encoding='utf-8') as fh:
        fh.write(output)
