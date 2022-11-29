from datetime import datetime, timedelta
from random import randint

from faker import Faker
from faker.providers import phone_number, address, date_time

from .config import data_path, to_ppath

import csv
import configparser

fake = Faker("it_IT")

fake.add_provider(phone_number)
fake.add_provider(address)
fake.add_provider(date_time)

ncells = 0
people = []

def generate(load: int):
    global ncells

    config = configparser.ConfigParser()
    config.read(to_ppath('config.ini'))

    ncells = int((config.getint('load', 'MAX_CELLS') * load) / 100)

    gen_start_time = datetime.now()

    print('[Info] inizio generazione dataset: ', gen_start_time.strftime('%d/%m/%Y %H:%M:%S'))

    gen_people(int((config.getint('load', 'MAX_PEOPLE') * load) / 100))
    gen_cells(ncells)
    gen_calls(int((config.getint('load', 'MAX_CALLS') * load) / 100))

    gen_end_time = datetime.now()
    print('[Info] fine generazione dataset: ', gen_end_time.strftime('%d/%m/%Y %H:%M:%S'), ' - tempo impiegato: ', (gen_end_time - gen_start_time).microseconds, 'ms')

def gen_people(size: int):
    with open(data_path("people.csv"), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['first_name', 'last_name', 'full_name', 'number'])

        for i in range(size):
            name = fake.name().split()

            #genera un numero univoco (simulazione di un do-while)
            while True:
                number = gen_fake_phone_number()
                if number not in people:
                    break

            writer.writerow([name[0], name[1], " ".join(name), number])
            people.append(number)

        file.close()


def gen_cells(size: int):
    global ncells

    with open(data_path("cells.csv"), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['cell_site', 'city', 'address', 'state'])

        for i in range(size):
            city = fake.city()
            address = fake.street_name()
            state = fake.current_country_code()

            writer.writerow([i, city, address, state])

        file.close()


def gen_calls(size: int):
    npeople = len(people)

    with open(data_path("calls.csv"), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['calling_number', 'called_number', 'start_date', 'end_date', 'duration', 'cell_site'])

        for i in range(size):
            caller = randint(0, npeople-1)

            #prende ripetutamente un numero dalla lista delle persone se il numero del chiamante è uguale a quello del chiamato
            while True:
                called = randint(0, npeople-1)
                if called != caller:
                    break

            duration = randint(0, 1000)
            cell_site = randint(0, ncells-1)

            #data di inizio [solo anno attuale]
            start_date = fake.date_time_this_year()

            #la data di fine della chiamata equivale alla data di inizio della chiamata + la durata(in secondi)
            end_date = start_date + timedelta(seconds=duration)

            writer.writerow([people[caller], people[called], int(round(datetime.timestamp(start_date))), int(round(datetime.timestamp(end_date))), duration, cell_site])
        file.close()

def gen_fake_phone_number() -> str:
    return f'3{fake.msisdn()[1:10]}'