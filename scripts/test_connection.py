import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

def test_connectivity():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()

        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) AS total_nodes")
            record = result.single()
            print(f"✅ Successfully connected to Neo4j AuraDB! Total nodes found: {record['total_nodes']}")

        driver.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connectivity()