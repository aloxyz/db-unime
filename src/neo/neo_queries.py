import csv
from datetime import datetime
from statistics import stdev
from time import time

from neo4j import GraphDatabase

from src.config import data_path


def run_queries(handle: GraphDatabase.driver, load: int):

    gt_start = int(round(datetime.timestamp(datetime(2022, 6, 1))))
    lt_start = int(round(datetime.timestamp(datetime(2022, 7, 1))))

    duration = 500

    queries = [
        "MATCH (c:call) WHERE c.start_date >" + str(gt_start) + " AND c.start_date < " + str(
            lt_start) + " RETURN c",
        "MATCH (c:call) WHERE c.start_date > " + str(gt_start) + " AND c.start_date < " + str(lt_start) + " AND c.duration >= " + str(duration) + " RETURN c",
        "MATCH (p:person)-[r:made_call]->(c:call) WHERE c.start_date >" + str(gt_start) + " AND c.start_date < " + str(
            lt_start) + " AND c.duration >= " + str(duration) + " RETURN c, r, p",
        "MATCH(p:person)-[r1:made_call]->(c:call)-[r2:located_in]->(ce:cell) WHERE c.start_date >" + str(gt_start) + " AND c.start_date < " + str(
            lt_start) + " AND c.duration >= " + str(duration) + " RETURN c,p,r1,r2,ce",

    ]

    for i in range(len(queries)):
        times = []
        with open(data_path('results\\neo\\' + str(load) + '\\query_'+ str(i+1) + '_load_' + str(load) + '.csv'), "w", newline="") as fq:
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


def run_query(handle: GraphDatabase.driver, query: list) -> float:
    start = time()
    with handle.session() as ses:
        ses.run(query)

    return time() - start