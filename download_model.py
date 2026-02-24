"""
Pre-download the embedding model for faster server startup.
Run this once before starting the API server.
"""
from sentence_transformers import SentenceTransformer

print("Downloading embedding model 'all-MiniLM-L6-v2'...")
print("This is a one-time download (~90MB)...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("\n Model downloaded successfully!")
print("You can now start the API server with: python api.py")
