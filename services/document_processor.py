from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import os

class DocumentProcessor:
    """Process documents using LangChain"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def load_pdf(self, file_path):
        """Load PDF using LangChain PyPDFLoader"""
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            
            # Extract text from all pages
            text = "\n\n".join([page.page_content for page in pages])
            return text, pages
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return "", []
    
    def load_docx(self, file_path):
        """Load DOCX using LangChain"""
        try:
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
            text = "\n\n".join([doc.page_content for doc in documents])
            return text, documents
        except Exception as e:
            print(f"Error loading DOCX: {e}")
            return "", []
    
    def load_txt(self, file_path):
        """Load TXT file"""
        try:
            loader = TextLoader(file_path)
            documents = loader.load()
            text = "\n\n".join([doc.page_content for doc in documents])
            return text, documents
        except Exception as e:
            print(f"Error loading TXT: {e}")
            return "", []
    
    def chunk_documents(self, text):
        """Split text into chunks using LangChain"""
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def process_uploaded_files(self, uploaded_files):
        """
        Process all uploaded files from Streamlit
        
        Args:
            uploaded_files: dict with keys: pitch_deck, transcripts, emails, updates
        
        Returns:
            dict with extracted text and chunks
        """
        extracted_data = {
            "pitch_deck": {"text": "", "chunks": []},
            "transcripts": [],
            "emails": [],
            "updates": []
        }
        
        # Process pitch deck (required)
        if uploaded_files.get('pitch_deck'):
            pitch_file = uploaded_files['pitch_deck']
            file_path = self._save_uploaded_file(pitch_file)
            
            text, _ = self.load_pdf(file_path)
            chunks = self.chunk_documents(text)
            
            extracted_data['pitch_deck'] = {
                "text": text,
                "chunks": chunks,
                "filename": pitch_file.name
            }
        
        # Process transcripts (optional)
        if uploaded_files.get('transcripts'):
            for transcript_file in uploaded_files['transcripts']:
                file_path = self._save_uploaded_file(transcript_file)
                text, _ = self._load_file_by_extension(file_path)
                chunks = self.chunk_documents(text)
                
                extracted_data['transcripts'].append({
                    "text": text,
                    "chunks": chunks,
                    "filename": transcript_file.name
                })
        
        # Process emails (optional)
        if uploaded_files.get('emails'):
            for email_file in uploaded_files['emails']:
                file_path = self._save_uploaded_file(email_file)
                text, _ = self._load_file_by_extension(file_path)
                chunks = self.chunk_documents(text)
                
                extracted_data['emails'].append({
                    "text": text,
                    "chunks": chunks,
                    "filename": email_file.name
                })
        
        # Process founder updates (optional)
        if uploaded_files.get('updates'):
            for update_file in uploaded_files['updates']:
                file_path = self._save_uploaded_file(update_file)
                text, _ = self._load_file_by_extension(file_path)
                chunks = self.chunk_documents(text)
                
                extracted_data['updates'].append({
                    "text": text,
                    "chunks": chunks,
                    "filename": update_file.name
                })
        
        return extracted_data
    
    def _save_uploaded_file(self, uploaded_file):
        """Save Streamlit uploaded file to disk"""
        from config import UPLOAD_FOLDER
        
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    
    def _load_file_by_extension(self, file_path):
        """Load file based on extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self.load_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self.load_docx(file_path)
        elif ext == '.txt':
            return self.load_txt(file_path)
        else:
            # Try as text
            return self.load_txt(file_path)