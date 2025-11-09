import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")



# Model Configuration
DEFAULT_LLM_PROVIDER = "groq"  
DEFAULT_MODEL = "llama-3.1-8b-instant"  

# Embedding Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 3

# Response Mode Configuration
CONCISE_MAX_TOKENS = 150
DETAILED_MAX_TOKENS = 1000

# ESG Scoring Weights
ESG_WEIGHTS = {
    "environmental": 0.35,
    "social": 0.35,
    "governance": 0.30
}

# ESG Risk Keywords
ESG_KEYWORDS = {
    "environmental": ["carbon", "emissions", "ghg", "renewable", "energy", "water", "waste", "pollution"],
    "social": ["diversity", "labor", "human rights", "safety", "community", "employee"],
    "governance": ["board", "ethics", "compliance", "transparency", "audit", "risk management"]
}