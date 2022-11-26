from faker import Faker
from .config import data_path

import csv

faker = Faker("it_IT")

def generate(size: tuple):
    gen_people(size[0])
    gen_cells(size[1])
    gen_cities(size[2])
    gen_calls(size[3])

def gen_people(size: int):
    with open(data_path("people.csv"), 'w') as file:
        writer = csv.writer(file)

        writer.writerow(['first_name', 'last_name', 'full_name', 'number'])

    for i in range(size):
        print("ciao ciao ciao ciao")

def gen_cells(size: int):
    pass
def gen_cities(size: int):
    pass
def gen_calls(size: int):
    pass