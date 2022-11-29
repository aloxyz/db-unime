import csv

from pymongo import MongoClient
from .mongo_queries import run_queries
from ..config import data_path
from csv import DictReader
from ..utils import to_dict

DATABASE="progettodb2"

def connect(ip: str = "localhost", port: int = 27017) -> MongoClient:
    connection = "mongodb://" + ip + ":" + str(port) + "/" + DATABASE
    return MongoClient(connection)

def reset(handle: MongoClient):
    handle.drop_database(DATABASE)

def load_data(handle: MongoClient):
    db = handle.progettodb2

    with open(data_path('cells.csv'), "r") as cfile:
        db.cells.insert_many(to_dict(list(DictReader(cfile))))

        cfile.close()

    with open(data_path('people.csv'), "r") as pfile:
        db.people.create_index("number", unique=True)
        db.people.insert_many(to_dict(list(DictReader(pfile))))

        pfile.close()

    with open(data_path('calls.csv'), "r") as cafile:
        db.calls.insert_many(to_dict(list(DictReader(cafile))))

        cafile.close()

    print("[Info - MONGO]: database caricato")

def exec(load: int, refresh: bool):
    handle = connect()

    if refresh:
        reset(handle)
        load_data(handle)


    #run_queries(handle)




