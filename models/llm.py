from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

class LLMManager:
    """Manages LLM provider"""
    
    def __init__(self, provider="groq", model_name=None):
        """
        Initialize LLM
        
        Args:
            provider (str): "groq" (others available but we're using Groq)
            model_name (str): Specific model name (optional)
        """
        self.provider = provider
        self.llm = self._initialize_llm(provider, model_name)
    
    def _initialize_llm(self, provider, model_name):
        """Initialize the LLM"""
        try:
            if not GROQ_API_KEY:
                raise ValueError("Groq API key not found in .env file")
            
            return ChatGroq(
                api_key=GROQ_API_KEY,
                model=model_name or "llama-3.1-8b-instant",
                temperature=0.3
            )
                
        except Exception as e:
            print(f"❌ Error initializing LLM: {e}")
            raise
    
    def generate_response(self, prompt, max_tokens=500):
        """
        Generate response from LLM
        
        Args:
            prompt (str): Input prompt
            max_tokens (int): Maximum tokens in response
            
        Returns:
            str: Generated response
        """
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return f"Error: {str(e)}"
    
    def get_provider_info(self):
        """Get current provider information"""
        return {
            "provider": self.provider,
            "model": getattr(self.llm, "model_name", "unknown")
        }

def get_llm(provider="groq", model_name=None):
    """
    Get LLM instance
    
    Args:
        provider (str): LLM provider
        model_name (str): Model name (optional)
        
    Returns:
        LLMManager: LLM manager instance
    """
    return LLMManager(provider, model_name)