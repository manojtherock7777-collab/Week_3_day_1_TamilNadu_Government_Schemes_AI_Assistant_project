import os
from langchain_neo4j import Neo4jGraph
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Initialize Neo4j connection
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database="a987b0aa"
)

# Comprehensive dataset of Tamil Nadu Government Welfare Schemes
tn_schemes_data = [
    {
        "department": "Agriculture - Farmers Welfare Department",
        "schemes": [
            {
                "name": "Kalaignarin All Village Integrated Agriculture Development Programme (KAVIADP)",
                "eligibility": "All farmers and rural residents in selected village panchayats.",
                "benefit": "Assistance for land development, horticulture crop cultivation, micro-irrigation, and farm ponds.",
                "category": "Agriculture"
            },
            {
                "name": "Chief Minister's Uzhavar Pathukappu Thittam",
                "eligibility": "Agricultural laborers and small/marginal farmers registered with the board.",
                "benefit": "Financial assistance for education of children, marriage assistance, maternity assistance, and accident/natural death relief.",
                "category": "Farmers Welfare"
            },
            {
                "name": "Free Electricity for Farming",
                "eligibility": "All agricultural landowners holding active agricultural power service connections in Tamil Nadu.",
                "benefit": "Free 3-phase electricity supply for agricultural pump sets.",
                "category": "Agriculture"
            }
        ]
    },
    {
        "department": "Social Welfare and Women Empowerment Department",
        "schemes": [
            {
                "name": "Kalaignar Magalir Urimai Thittam",
                "eligibility": "Women aged 21 and above in eligible families with annual household income below specified limits, owning residential houses under certain criteria.",
                "benefit": "Monthly financial assistance of ₹1,000 directly credited to bank accounts.",
                "category": "Women Welfare"
            },
            {
                "name": "Moovalur Ramamritham Ammaiyar Higher Education Assurance Scheme (Pudhumai Penn Thittam)",
                "eligibility": "Girl students who studied from Class 6 to Class 12 in Government schools and enrolled in higher education.",
                "benefit": "Monthly financial assistance of ₹1,000 directly transferred to students' bank accounts until graduation.",
                "category": "Education & Women Empowerment"
            },
            {
                "name": "Dr. Muthulakshmi Reddy Paternity Benefit Scheme",
                "eligibility": "Pregnant and lactating mothers for up to two deliveries (focusing on economically weaker sections).",
                "benefit": "Financial assistance of ₹18,000 given in installments for nutrition and health care.",
                "category": "Health & Maternity"
            }
        ]
    },
    {
        "department": "Backward Classes, Most Backward Classes and Minorities Welfare Department",
        "schemes": [
            {
                "name": "Free Laptop Distribution Scheme",
                "eligibility": "Students studying in Government and Government-aided higher secondary schools and colleges.",
                "benefit": "Free laptop computers to aid digital learning and higher education.",
                "category": "Education"
            },
            {
                "name": "Educational Loan Subsidy for BC/MBC/DNC Students",
                "eligibility": "Students belonging to Backward Classes (BC), Most Backward Classes (MBC), and Denotified Communities (DNC) pursuing higher education with annual family income below ₹2.5 Lakhs.",
                "benefit": "Subsidy on educational loans taken through cooperative banks and financial corporations.",
                "category": "Education"
            }
        ]
    },
    {
        "department": "Labour Welfare and Skill Development Department",
        "schemes": [
            {
                "name": "Tamil Nadu Construction Workers Welfare Board Assistance",
                "eligibility": "Registered construction workers with the board.",
                "benefit": "Accident insurance, educational assistance for children, marriage assistance, and pension benefits.",
                "category": "Labour Welfare"
            },
            {
                "name": "Naan Mudhalvan Scheme",
                "eligibility": "Youth and students across schools, colleges, and polytechnics in Tamil Nadu.",
                "benefit": "Skill training, language training, coding bootcamps, and competitive exam coaching (UPSC, TNPSC) with placement support.",
                "category": "Skill Development"
            }
        ]
    }
]

print("🔄 Clearing existing graph nodes to load comprehensive scheme database...")
graph.query("MATCH (n) DETACH DELETE n")

print("📥 Ingesting comprehensive Tamil Nadu Government Schemes into Neo4j...")

for dept in tn_schemes_data:
    dept_name = dept["department"]
    for scheme in dept["schemes"]:
        query = """
        MERGE (d:Department {name: $dept_name})
        MERGE (s:Scheme {name: $scheme_name})
        SET s.eligibility = $eligibility,
            s.benefit = $benefit,
            s.category = $category
        MERGE (s)-[:OFFERED_BY]->(d)
        """
        graph.query(
            query,
            params={
                "dept_name": dept_name,
                "scheme_name": scheme["name"],
                "eligibility": scheme["eligibility"],
                "benefit": scheme["benefit"],
                "category": scheme["category"]
            }
        )
        print(f"Added Scheme: {scheme['name']} under {dept_name}")

print("✅ Comprehensive Data Ingestion Complete!")