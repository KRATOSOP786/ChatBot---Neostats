



import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

class EmbeddingModel:
    """Handles text embeddings using transformers"""
    
    def __init__(self):
        """Initialize the embedding model"""
        try:
            # Use a small, fast model
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.eval()
            print(f"✅ Embedding model loaded: {model_name}")
        except Exception as e:
            print(f"❌ Error loading embedding model: {e}")
            raise
    
    def _mean_pooling(self, model_output, attention_mask):
        """Mean pooling to get sentence embeddings"""
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def encode_text(self, text):
        """Encode a single text"""
        try:
            encoded_input = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt', max_length=512)
            
            with torch.no_grad():
                model_output = self.model(**encoded_input)
            
            embedding = self._mean_pooling(model_output, encoded_input['attention_mask'])
            embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)
            
            return embedding[0].numpy()
        except Exception as e:
            print(f"❌ Error encoding text: {e}")
            return None
    
    def encode_texts(self, texts):
        """Encode multiple texts"""
        try:
            encoded_input = self.tokenizer(texts, padding=True, truncation=True, return_tensors='pt', max_length=512)
            
            with torch.no_grad():
                model_output = self.model(**encoded_input)
            
            embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
            
            return embeddings.numpy()
        except Exception as e:
            print(f"❌ Error encoding texts: {e}")
            return None
    
    def get_embedding_dimension(self):
        """Get embedding dimension"""
        return 384

# Global instance
_embedding_model = None

def get_embedding_model():
    """Get or create the global embedding model instance"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = EmbeddingModel()
    return _embedding_model