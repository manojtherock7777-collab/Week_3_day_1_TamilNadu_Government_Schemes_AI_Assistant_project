import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

print("Checking databases in your Neo4j Aura instance...")
try:
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    )
    with driver.session() as session:
        result = session.run("SHOW DATABASES")
        print("\nAvailable Databases:")
        for record in result:
            print(f"- Name: {record['name']}, Default: {record.get('default', False)}, Status: {record.get('currentStatus', 'N/A')}")
    driver.close()
except Exception as e:
    print(f"❌ Error: {e}")