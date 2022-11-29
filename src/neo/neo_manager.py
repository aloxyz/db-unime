from neo4j import GraphDatabase

def connect(ip: str = "localhost", port: int = 7687) -> GraphDatabase.driver:
    return GraphDatabase.driver("neo4j://" + ip + ":" + str(port), auth=("neo4j", "neo4j"))

def reset(driver: GraphDatabase.driver):
    driver.session().run("MATCH(n) DETACH DELETE n")

def load_data(driver: GraphDatabase.driver):
    pass

def exec(load: int, refresh: bool):
    handle = connect()

    if refresh:
        reset(handle)
        #load_data(handle)


    pass