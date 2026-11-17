import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph
from nemoguardrails import LLMRails, RailsConfig
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize FastAPI app
app = FastAPI(title="TN Government Schemes GraphRAG API")

# 2. Initialize Neo4j Graph with your Aura database name
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    database="a987b0aa"
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 3. Initialize NeMo Guardrails safely
try:
    config = RailsConfig.from_path("./backend/guardrails_config")
    rails = LLMRails(config)
except Exception as e:
    print(f"⚠️ Guardrails warning: {e}")
    rails = None

class QueryRequest(BaseModel):
    query: str
    language: str = "en"  # "en" or "ta"

# 4. Define chat endpoint with direct Knowledge Graph context injection
@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        # NeMo Guardrail validation check (if active)
        if rails:
            guardrail_response = await rails.generate_async(
                messages=[{"role": "user", "content": request.query}]
            )
            response_text = guardrail_response.get("content", "")
            if "specialized only in" in response_text or "மட்டுமே பதிலளிக்க முடியும்" in response_text:
                return {"response": response_text}
        
        # Fetch all schemes from Neo4j Knowledge Graph
        cypher_query = """
        MATCH (s:Scheme)-[:OFFERED_BY]->(d:Department)
        RETURN s.name AS name, s.category AS category, s.eligibility AS eligibility, s.benefit AS benefit, d.name AS department
        """
        results = graph.query(cypher_query)
        
        # Build context from graph data
        context_lines = []
        for r in results:
            context_lines.append(
                f"Scheme: {r['name']}\nDepartment: {r['department']}\nCategory: {r['category']}\nEligibility: {r['eligibility']}\nBenefit: {r['benefit']}\n"
            )
        context = "\n".join(context_lines)
        
        # Prompt LLM with the complete knowledge graph context
        prompt = f"""
        You are an expert assistant on Tamil Nadu Government Welfare Schemes. 
        Answer the user's query thoroughly and accurately using ONLY the following schemes context retrieved from the Knowledge Graph:
        
        {context}
        
        User Query: {request.query}
        """
        if request.language == "ta":
            prompt += " Reply fluently in Tamil language."
            
        result = llm.invoke(prompt).content
        return {"response": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))