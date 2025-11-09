# import faiss
from langchain_community.vectorstores import faiss
import numpy as np
from models.embeddings import get_embedding_model
from config.config import TOP_K_RESULTS

class RAGEngine:
    """Retrieval-Augmented Generation Engine"""
    
    def __init__(self):
        """Initialize RAG engine"""
        self.embedding_model = get_embedding_model()
        self.index = None
        self.chunks = []
        self.dimension = self.embedding_model.get_embedding_dimension()
    
    def build_index(self, text_chunks):
        """
        Build FAISS index from text chunks
        
        Args:
            text_chunks (list): List of text chunks
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not text_chunks:
                print("❌ No text chunks provided")
                return False
            
            self.chunks = text_chunks
            
            # Create embeddings for all chunks
            print(f"🔄 Creating embeddings for {len(text_chunks)} chunks...")
            embeddings = self.embedding_model.encode_texts(text_chunks)
            
            if embeddings is None:
                return False
            
            # Create FAISS index
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(embeddings.astype('float32'))
            
            print(f"✅ FAISS index built with {len(text_chunks)} vectors")
            return True
            
        except Exception as e:
            print(f"❌ Error building index: {e}")
            return False
    
    def retrieve(self, query, top_k=TOP_K_RESULTS):
        """
        Retrieve relevant chunks for a query
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            list: List of relevant text chunks
        """
        try:
            if self.index is None or not self.chunks:
                print("❌ Index not built yet")
                return []
            
            # Create query embedding
            query_embedding = self.embedding_model.encode_text(query)
            if query_embedding is None:
                return []
            
            # Search in FAISS index
            query_vector = np.array([query_embedding]).astype('float32')
            distances, indices = self.index.search(query_vector, top_k)
            
            # Get relevant chunks
            relevant_chunks = [self.chunks[idx] for idx in indices[0] if idx < len(self.chunks)]
            
            print(f"✅ Retrieved {len(relevant_chunks)} relevant chunks")
            return relevant_chunks
            
        except Exception as e:
            print(f"❌ Error retrieving chunks: {e}")
            return []
    
    def clear_index(self):
        """Clear the current index"""
        self.index = None
        self.chunks = []
        print("✅ Index cleared")

# Global RAG engine instance
_rag_engine = None

def get_rag_engine():
    """Get or create global RAG engine instance"""
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine