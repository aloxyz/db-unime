from time import time
from pymongo import MongoClient

from ..config import data_path

def run_queries(handle: MongoClient):
    queries = [

    ]

    #with open(data_path("results\\mongo_result"))

    pass

def run_query(handle: MongoClient, query: list)-> float:
    start = time()
    handle.get_default_database().aggregate(query)

    return time() - start