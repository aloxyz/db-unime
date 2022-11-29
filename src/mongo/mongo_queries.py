import csv
from datetime import datetime
from statistics import stdev
from time import time
from pymongo import MongoClient

from ..config import data_path

def run_queries(handle: MongoClient, load: int):

    gt_start = int(round(datetime.timestamp(datetime(2022, 6, 1))))
    lt_start = int(round(datetime.timestamp(datetime(2022, 7, 1))))
    duration = 500

    queries = [
        #1° query
        [
            {
                "$match": {
                    "start_date": {
                        "$gte": gt_start,
                        "$lt": lt_start
                    },
                    "duration": {
                        "$gte": duration
                    }
                }
            },
        ],
        #2° query
        [
            {
                "$match": {
                    "start_date": {
                        "$gte": gt_start,
                        "$lt": lt_start
                    },
                    "duration": {
                        "$gte": duration
                    }
                }
            },
            {
                "$lookup": {
                    "from": "people",
                    "localField": "calling_number",
                    "foreignField": "number",
                    "as": "caller"
                }
            }
        ],
        #3° query
        [
            {
                "$match": {
                    "start_date": {
                        "$gte": gt_start,
                        "$lt": lt_start
                    },
                    "duration": {
                        "$gte": duration
                    }
                }
            },
            {
                "$lookup": {
                    "from": "people",
                    "localField": "calling_number",
                    "foreignField": "number",
                    "as": "caller"
                }
            },
            {
                "$lookup": {
                    "from": "cells",
                    "localField": "cell_site",
                    "foreignField": "cell_site",
                    "as": "cell"
                }
            }
        ],
        #4° query
        [
            {
                "$match": {
                    "start_date": {
                        "$gte": gt_start,
                        "$lt": lt_start
                    },
                    "duration": {
                        "$gte": duration
                    },
                }
            },
            {
                "$lookup": {
                    "from": "people",
                    "localField": "calling_number",
                    "foreignField": "number",
                    "as": "caller"
                }
            },
            {
                "$lookup": {
                    "from": "people",
                    "localField": "called_number",
                    "foreignField": "number",
                    "as": "called"
                }
            },
            {
                "$lookup": {
                    "from": "cells",
                    "localField": "cell_site",
                    "foreignField": "cell_site",
                    "as": "cell"
                }
            }
        ]
    ]

    for i in range(len(queries)):
        times = []
        with open(data_path('results\\mongo\\' + str(load) + '\\query_'+ str(i+1) + '_load_' + str(load) + '.csv'), "w", newline="") as fq:
            writer = csv.writer(fq)
            writer.writerow(['Prima Run', str(run_query(handle, queries[i]))])

            for j in range(30):
                times += [run_query(handle, queries[i])]
                writer.writerow([str(j+1), times[j]])

            avg = sum(times) / 30
            std = stdev(times)

            writer.writerow(['Media', str(avg)])
            writer.writerow(['Dev. Std.', str(std)])

            fq.close()

def run_query(handle: MongoClient, query: list)-> float:
    start = time()
    handle.get_default_database().calls.aggregate(query)

    return time() - start