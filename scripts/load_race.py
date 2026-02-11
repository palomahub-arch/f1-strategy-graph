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
fastf1.Cache.enable_cache("/workspaces/f1-strategy-graph/cache")

f1_session = fastf1.get_session(2024, "Monaco", "R")
f1_session.load()

results = f1_session.results

# -------- INSERT FUNCTION --------
def insert_data(tx, driver_name, team_name, position):
    tx.run("""
        MERGE (d:Driver {name:$driver})
        MERGE (t:Team {name:$team})
        MERGE (r:Race {name:$race})

        MERGE (d)-[:DRIVES_FOR]->(t)
        MERGE (d)-[:FINISHED {position:$pos}]->(r)
    """,
    driver=driver_name,
    team=team_name,
    race="Monaco GP 2024",
    pos=int(position)
    )

# -------- RUN INSERTS --------
with driver.session() as session_db:
    for _, row in results.iterrows():
        session_db.execute_write(
            insert_data,
            row["FullName"],
            row["TeamName"],
            row["Position"]
        )

print("✅ Dados reais carregados no Neo4j!")

driver.close()
