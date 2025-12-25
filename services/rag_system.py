import chromadb
from chromadb.config import Settings
import uuid
import os
from langchain_huggingface import HuggingFaceEndpointEmbeddings
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
HF_TOKEN = os.getenv('HF_TOKEN')
UPLOAD_FOLDER = "uploads"
DATA_FOLDER = "data"
CHROMA_DB_PATH = "./data/chroma_db"

class RAGSystem:
    """RAG system using ChromaDB and Gemini embeddings"""
    
    def __init__(self):
        # Initialize ChromaDB
        self.client = chromadb.Client(Settings(
            persist_directory=CHROMA_DB_PATH,
            anonymized_telemetry=False
        ))
        
        # Initialize Gemini embeddings through LangChain
        self.embeddings = HuggingFaceEndpointEmbeddings(
                model="sentence-transformers/all-MiniLM-L6-v2",  # Use a proper embedding model
                 task="feature-extraction",
                  huggingfacehub_api_token=HF_TOKEN
)
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection("startup_documents")
        except:
            self.collection = self.client.create_collection(
                name="startup_documents",
                metadata={"description": "Startup analysis documents"}
            )
    
    def add_documents(self, extracted_data, startup_id):
        """
        Add all documents to vector database
        
        Args:
            extracted_data: dict from DocumentProcessor
            startup_id: unique identifier for this startup
        """
        all_chunks = []
        metadatas = []
        ids = []
        
        # Add pitch deck chunks
        if extracted_data['pitch_deck']['chunks']:
            for i, chunk in enumerate(extracted_data['pitch_deck']['chunks']):
                all_chunks.append(chunk)
                metadatas.append({
                    "startup_id": startup_id,
                    "doc_type": "pitch_deck",
                    "chunk_index": i,
                    "filename": extracted_data['pitch_deck']['filename']
                })
                ids.append(f"{startup_id}_pitch_{i}")
        
        # Add transcript chunks
        for doc_idx, transcript in enumerate(extracted_data['transcripts']):
            for i, chunk in enumerate(transcript['chunks']):
                all_chunks.append(chunk)
                metadatas.append({
                    "startup_id": startup_id,
                    "doc_type": "transcript",
                    "doc_index": doc_idx,
                    "chunk_index": i,
                    "filename": transcript['filename']
                })
                ids.append(f"{startup_id}_transcript_{doc_idx}_{i}")
        
        # Add email chunks
        for doc_idx, email in enumerate(extracted_data['emails']):
            for i, chunk in enumerate(email['chunks']):
                all_chunks.append(chunk)
                metadatas.append({
                    "startup_id": startup_id,
                    "doc_type": "email",
                    "doc_index": doc_idx,
                    "chunk_index": i,
                    "filename": email['filename']
                })
                ids.append(f"{startup_id}_email_{doc_idx}_{i}")
        
        # Add update chunks
        for doc_idx, update in enumerate(extracted_data['updates']):
            for i, chunk in enumerate(update['chunks']):
                all_chunks.append(chunk)
                metadatas.append({
                    "startup_id": startup_id,
                    "doc_type": "update",
                    "doc_index": doc_idx,
                    "chunk_index": i,
                    "filename": update['filename']
                })
                ids.append(f"{startup_id}_update_{doc_idx}_{i}")
        
        # Create embeddings and add to ChromaDB
        if all_chunks:
            # Create embeddings using LangChain
            embeddings_list = self.embeddings.embed_documents(all_chunks)
            
            # Add to ChromaDB
            self.collection.add(
                documents=all_chunks,
                embeddings=embeddings_list,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Added {len(all_chunks)} chunks to RAG system")
            return len(all_chunks)
        
        return 0
    
    def query(self, question, startup_id, n_results=5):
        """
        Query the RAG system
        
        Args:
            question: The question to ask
            startup_id: Filter by startup
            n_results: Number of results to return
        
        Returns:
            Combined context from relevant chunks
        """
        try:
            # Create query embedding
            query_embedding = self.embeddings.embed_query(question)
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where={"startup_id": startup_id}
            )
            
            if results['documents'] and results['documents'][0]:
                # Combine relevant chunks
                context = "\n\n---\n\n".join(results['documents'][0])
                return context
            
            return ""
            
        except Exception as e:
            print(f"❌ Error querying RAG: {e}")
            return ""
    
    def query_by_doc_type(self, question, startup_id, doc_type, n_results=3):
        """Query specific document type"""
        try:
            query_embedding = self.embeddings.embed_query(question)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where={
                    "$and": [
                        {"startup_id": startup_id},
                        {"doc_type": doc_type}
                    ]
                }
            )
            
            if results['documents'] and results['documents'][0]:
                context = "\n\n---\n\n".join(results['documents'][0])
                return context
            
            return ""
            
        except Exception as e:
            print(f"❌ Error querying by doc type: {e}")

            return ""


