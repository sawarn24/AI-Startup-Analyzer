import os

# ============================================
# API KEYS (Replace with your actual keys)
# ============================================

GEMINI_API_KEY = "AIzaSyA8AxtkmGmMLR4oOicmsaM536_CZizehjM"
GOOGLE_SEARCH_API_KEY = "AIzaSyA8AxtkmGmMLR4oOicmsaM536_CZizehjM"
SEARCH_ENGINE_ID = "b34777b2b953e44c6"
HF_TOKEN="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"

# ============================================
# GOOGLE CLOUD
# ============================================

PROJECT_ID = "startup-analyzer-hackathon"
LOCATION = "us-central1"

# ============================================
# FOLDERS
# ============================================

UPLOAD_FOLDER = "uploads"
DATA_FOLDER = "data"
CHROMA_DB_PATH = "./data/chroma_db"

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)

# ============================================
# FIRESTORE (Optional - for saving results)
# ============================================

FIRESTORE_COLLECTION = "startup_analyses"