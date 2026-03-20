import os
import sys
import json
from typing import List, Dict

# Add root to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import faiss # type: ignore
    import numpy as np # type: ignore
    from sentence_transformers import SentenceTransformer # type: ignore
except ImportError:
    pass

class VectorKnowledgeBase:
    def __init__(self, db_path='data/kb.json', index_path='data/kb_index.faiss'):
        self.db_path = db_path
        self.index_path = index_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.knowledge = self._load_db()
        self.index = self._load_index()
    
    def _load_db(self) -> List[Dict]:
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return []
    
    def _load_index(self):
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        return faiss.IndexFlatL2(384) # Dim 384 for all-MiniLM-L6-v2

    def store_knowledge(self, task: str, solution: str):
        """Stores a task and its solution in the vector database."""
        embedding = self.model.encode(task)
        entry = {
            "task": task,
            "solution": solution,
            "embedding": embedding.tolist()
        }
        self.knowledge.append(entry)
        
        # Update FAISS
        embeddings = np.array([e["embedding"] for e in self.knowledge])
        self.index = faiss.IndexFlatL2(384)
        self.index.add(embeddings.astype('float32'))
        faiss.write_index(self.index, self.index_path)
        
        # Save JSON
        with open(self.db_path, 'w') as f:
            json.dump(self.knowledge, f)
        
        task_snippet = str(task)[:50] # type: ignore
        print(f"✅ Stored task: {task_snippet}...")

    def retrieve_knowledge(self, query: str, top_k: int = 1) -> List[Dict]:
        """Retrieves similar past solutions from the knowledge base."""
        if not self.knowledge or self.index.ntotal == 0:
            return []
            
        embedding = self.model.encode(query)
        distances, indices = self.index.search(np.array([embedding]).astype('float32'), top_k)
        first_indices = list(indices[0]) # type: ignore
        results = []
        for i, idx in enumerate(first_indices):
            if idx >= 0 and idx < len(self.knowledge):
                entry = self.knowledge[idx]
                results.append({
                    "task": entry["task"],
                    "solution": entry["solution"],
                    "similarity": float(1 - distances[0][i]/2) if distances[0][i] > 0 else 1.0 # type: ignore
                })
        return results

# Global instance for easier access from other modules
kb = VectorKnowledgeBase()

def store_knowledge(task, solution):
    kb.store_knowledge(task, solution)

def retrieve_knowledge(query):
    return kb.retrieve_knowledge(query)
