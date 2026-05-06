import os
import json
import glob
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_smosu.build_index")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_CONHECIMENTO_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "base_conhecimento")
INDEX_PATH = os.path.join(SCRIPT_DIR, "vector_index.faiss")
METADATA_PATH = os.path.join(SCRIPT_DIR, "vector_metadata.pkl")

# Model choice: Multilingual support is essential for Portuguese
MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'

def load_documents():
    documents = []
    
    # 1. Load Markdown and Text files
    files = glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.md")) + \
            glob.glob(os.path.join(BASE_CONHECIMENTO_DIR, "*.txt"))
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple chunking: split by double newlines (paragraphs/sections)
                chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 50]
                for chunk in chunks:
                    documents.append({
                        "text": chunk,
                        "source": os.path.basename(filepath)
                    })
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")

    # 2. Load Codex Legal (JSON) - Specific logic to extract articles/parameters
    codex_path = os.path.join(BASE_CONHECIMENTO_DIR, "codex_legal.json")
    if os.path.exists(codex_path):
        try:
            with open(codex_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Process parameters_zonais
                if "parametros_zonais" in data:
                    for zona, info in data["parametros_zonais"].items():
                        text = f"Zona: {zona}\n{json.dumps(info, indent=2, ensure_ascii=False)}"
                        documents.append({
                            "text": text,
                            "source": "codex_legal.json (parametros_zonais)"
                        })
                # Other keys
                for key, value in data.items():
                    if key == "parametros_zonais": continue
                    text = f"Assunto: {key}\n{str(value)}"
                    documents.append({
                        "text": text,
                        "source": f"codex_legal.json ({key})"
                    })
        except Exception as e:
            logger.error(f"Error reading codex_legal.json: {e}")

    # 3. Load Geo Oliveira (JSON)
    geo_path = os.path.join(BASE_CONHECIMENTO_DIR, "geo_oliveira.json")
    if os.path.exists(geo_path):
        try:
            with open(geo_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for key, valor in data.items():
                        text = f"Local/Zona: {key}\nIndices: {json.dumps(valor, indent=2, ensure_ascii=False)}"
                        documents.append({
                            "text": text,
                            "source": "geo_oliveira.json"
                        })
        except Exception as e:
            logger.error(f"Error reading geo_oliveira.json: {e}")

    return documents

def build_index():
    logger.info("Loading documents...")
    docs = load_documents()
    if not docs:
        logger.error("No documents found to index.")
        return

    logger.info(f"Loaded {len(docs)} chunks. Initializing model {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    
    logger.info("Generating embeddings (this may take a minute)...")
    texts = [d['text'] for d in docs]
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # FAISS Index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    logger.info(f"Saving index to {INDEX_PATH}...")
    faiss.write_index(index, INDEX_PATH)
    
    logger.info(f"Saving metadata to {METADATA_PATH}...")
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(docs, f)
        
    logger.info("Index build complete!")

if __name__ == "__main__":
    build_index()
