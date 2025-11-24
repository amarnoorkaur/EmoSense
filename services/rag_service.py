"""
RAG Service for Market Research Document Retrieval
Uses ChromaDB for vector storage and semantic search
"""
import os
import streamlit as st
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer


# Singleton instance
_rag_instance = None


class MarketResearchRAG:
    """
    Retrieval-Augmented Generation service for market research documents
    """
    
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        """
        Initialize the RAG system with ChromaDB
        
        Args:
            persist_directory: Directory to persist the vector database
        """
        self.persist_directory = persist_directory
        self.collection_name = "market_research"
        
        # Initialize ChromaDB client with memory optimization
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load embedding model (cached)
        self.embedding_model = self._load_embedding_model()
    
    @staticmethod
    @st.cache_resource
    def _load_embedding_model():
        """Load sentence transformer model for embeddings"""
        return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def ingest_document(self, 
                       text: str, 
                       metadata: Dict[str, Any],
                       doc_id: str = None):
        """
        Ingest a single document into the vector database
        
        Args:
            text: Document text content
            metadata: Document metadata (title, source, date, category, etc.)
            doc_id: Optional document ID (auto-generated if not provided)
        """
        if not text or not text.strip():
            return
        
        # Generate embedding
        embedding = self.embedding_model.encode(text).tolist()
        
        # Auto-generate ID if not provided
        if not doc_id:
            doc_id = f"doc_{self.collection.count() + 1}"
        
        # Add to collection
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
    
    def ingest_documents_from_folder(self, folder_path: str):
        """
        Ingest all text/markdown documents from a folder
        
        Args:
            folder_path: Path to folder containing research documents
        """
        folder = Path(folder_path)
        if not folder.exists():
            print(f"⚠️ Folder not found: {folder_path}")
            return
        
        # Supported file types
        supported_extensions = ['.txt', '.md', '.markdown']
        
        for file_path in folder.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract metadata from filename/path
                    metadata = {
                        "filename": file_path.name,
                        "source": str(file_path.relative_to(folder)),
                        "category": file_path.parent.name,
                        "file_type": file_path.suffix
                    }
                    
                    # Ingest document
                    doc_id = f"doc_{file_path.stem}"
                    self.ingest_document(content, metadata, doc_id)
                    
                    print(f"✅ Ingested: {file_path.name}")
                
                except Exception as e:
                    print(f"❌ Error ingesting {file_path.name}: {e}")
    
    def search_relevant_research(self, 
                                 query: str, 
                                 emotion: str = None,
                                 n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant market research based on query and emotion
        
        Args:
            query: Search query (text summary or keywords)
            emotion: Optional emotion filter
            n_results: Number of results to return
            
        Returns:
            List of relevant research documents with metadata
        """
        # Check if collection is empty
        if self.collection.count() == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Build where filter if emotion provided
        where_filter = None
        if emotion:
            where_filter = {"emotion_tag": emotion}
        
        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count()),
            where=where_filter if where_filter else None
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "relevance_score": 1 - results['distances'][0][i] if results['distances'] else 0.0
                })
        
        return formatted_results
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector database"""
        return {
            "total_documents": self.collection.count(),
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory
        }
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )


@st.cache_resource
def get_rag_service():
    """
    Get cached RAG service instance
    
    Returns:
        MarketResearchRAG instance
    """
    return MarketResearchRAG()


def initialize_rag_with_defaults():
    """
    Initialize RAG system with default market research documents
    """
    rag = get_rag_service()
    
    # Check if already initialized
    if rag.collection.count() > 0:
        return rag
    
    # Ingest documents from market research folder
    research_folder = "./data/market_research"
    if os.path.exists(research_folder):
        rag.ingest_documents_from_folder(research_folder)
    
    return rag
