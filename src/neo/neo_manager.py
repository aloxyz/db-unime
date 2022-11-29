from neo4j import GraphDatabase
from .neo_queries import run_queries

def connect(ip: str = "localhost", port: int = 7687) -> GraphDatabase.driver:
    try:
        driver = GraphDatabase.driver("neo4j://" + ip + ":" + str(port), auth=("neo4j", "progetto"))
    except Exception as e:
        print("Errore durante la creazione del driver ", e)

    return driver

def reset(driver: GraphDatabase.driver):
    driver.session().run("MATCH(n) DETACH DELETE n")

def load_data(driver: GraphDatabase.driver):
    load = [
        "LOAD CSV WITH HEADERS FROM 'file:///cells.csv' AS row \
                 CREATE (n:cell {cell_site:toInteger(row.cell_site), state:row.state, city:row.City, address:row.address})",

        "LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row \
         CREATE(p:person \
         {first_name: row.first_name, last_name: row.last_name, full_name: row.full_name, number: toInteger(row.number)})",

        "LOAD CSV WITH HEADERS FROM 'file:///calls.csv' AS row \
         CREATE (n:call {calling_number:toInteger(row.calling_number), called_number:toInteger(row.called_number), \
         start_date:toInteger(row.start_date), end_date:toInteger(row.end_date), duration:toInteger(row.duration), \
         cell_site:toInteger(row.cell_site)})",

        "MATCH (p:person), (c:call) \
         WHERE p.number = c.calling_number \
         CREATE (p)-[r:made_call]->(c)",

        "MATCH (p:person), (c:call) \
         WHERE p.number = c.called_number \
         CREATE (c)-[r:received_call]->(p)",

        "MATCH (c1:call), (c2:cell) \
         WHERE c1.cell_site = c2.cell_site \
         MERGE (c1)-[r:located_in]->(c2)"
    ]

    with driver.session() as ses:
        #caricamento file csv
        ses.run(load[0])
        ses.run(load[1])
        ses.run(load[2])

        #creazione archi
        ses.run(load[3])
        ses.run(load[4])
        ses.run(load[5])

def exec(load: int, refresh: bool):
    handle = connect()

    if refresh:
        reset(handle)
        load_data(handle)

    run_queries(handle, load)
