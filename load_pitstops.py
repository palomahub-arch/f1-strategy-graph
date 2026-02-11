import fastf1
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load env vars
load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# -------- LOAD F1 DATA --------

fastf1.Cache.enable_cache("cache")

# -------- LOAD SESSION --------
f1_session = fastf1.get_session(2024, "Monaco", "R")
f1_session.load()

pitstops = f1_session.laps[["Driver", "PitInTime", "PitOutTime", "LapNumber"]]
pitstops = pitstops.dropna()

# -------- INSERT PITSTOPS --------
def insert_pitstop(tx, driver_code, lap):
    tx.run("""
        MATCH (d:Driver {name:$driver})
        MATCH (r:Race {name:$race})

        MERGE (d)-[:PIT_STOP {lap:$lap}]->(r)
    """,
    driver=driver_code,
    race="Monaco GP 2024",
    lap=int(lap)
    )

with driver.session() as session_db:
    for _, row in pitstops.iterrows():
        session_db.execute_write(
            insert_pitstop,
            row["Driver"],
            row["LapNumber"]
        )

print("✅ Pitstops carregados no Neo4j!")

driver.close()
