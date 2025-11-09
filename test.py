import os
print("Before load_dotenv:", os.getenv("GROQ_API_KEY"))

from dotenv import load_dotenv
load_dotenv()

print("After load_dotenv:", os.getenv("GROQ_API_KEY"))


# Load .env
load_dotenv()

# Get the key DIRECTLY
api_key = os.getenv("GROQ_API_KEY")
print(f"API Key: '{api_key}'")
print(f"Raw value from .env: '{api_key}'")
print(f"Length: {len(api_key) if api_key else 0}")
print(f"First 15 chars: {api_key[:15] if api_key else 'NONE'}")

# Clean it
api_key_clean = api_key.strip() if api_key else ""
print(f"\nCleaned: '{api_key_clean[:15]}...'")

# Now test Groq with cleaned key
from langchain_groq import ChatGroq

try:
    llm = ChatGroq(
        api_key=api_key_clean,
        model="llama-3.1-8b-instant",
        temperature=0.3
    )
    
    print("\n🔄 Calling Groq API...")
    response = llm.invoke("Say hello")
    print(f"✅ SUCCESS! Response: {response.content}")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")