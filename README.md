# 🏎️ F1 Strategy Graph Analytics

A graph-based analytics project using **Neo4j Aura + FastF1 API** to model Formula 1 race strategy.

This project transforms real F1 race data into a connected graph structure, enabling powerful insights into:

- Pit stop strategy
- Tyre stints
- Driver-team performance
- Undercut vs Overcut patterns

---

## 🚀 Tech Stack

- **Python**
- **FastF1 API**
- **Neo4j Aura (Graph Database)**
- **Cypher Query Language**
- **Pandas**

---

## 📌 Graph Model

### Nodes

- `Driver`
- `Team`
- `Race`
- `Circuit`
- `Stint` *(coming next)*
- `PitStop`

### Relationships

- `(Driver)-[:DRIVES_FOR]->(Team)`
- `(Driver)-[:FINISHED]->(Race)`
- `(Race)-[:HELD_AT]->(Circuit)`
- `(Driver)-[:PIT_STOP]->(Race)`

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/palomahub-arch/f1-strategy-graph
cd f1-strategy-graph
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file:
```
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

## 🏁 Load Race Data into Neo4j

Run:

```
python scripts/load_race.py
```

Expected output:

```
✅ Monaco 2024 race results loaded into Neo4j!
```

## 🔍 Example Query
Fastest pit stops in the race

```cypher
MATCH (d:Driver)-[p:PIT_STOP]->(r:Race)
RETURN d.name, p.lap
ORDER BY p.lap ASC;
```

## 📈 Roadmap

 - Load race results
 - Connect drivers and teams
 - Insert pit stop events
 - Add tyre stint modeling
 - Undercut detection algorithm
 - Streamlit dashboard visualization
 - Multi-race season graph

 ## ✨ Author

Built by Paloma Cordeiro