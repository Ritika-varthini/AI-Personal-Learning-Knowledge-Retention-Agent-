import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os
from typing import List, Dict

class KnowledgeBase:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = self._init_index()
        self.knowledge = self._load_kb()
    
    def _init_index(self):
        index_path = 'data/kb_index.faiss'
        os.makedirs('data', exist_ok=True)
        if os.path.exists(index_path):
            return faiss.read_index(index_path)
        return faiss.IndexFlatL2(384)
    
    def _load_kb(self) -> List[Dict]:
        kb_path = 'data/kb.json'
        if os.path.exists(kb_path):
            with open(kb_path, 'r') as f:
                return json.load(f)
        return []
    
    def save_lesson(self, task_id: str, description: str, solution: str):
        """Save to KB"""
        entry = {
            "task_id": task_id,
            "description": description,
            "solution": solution,
            "embedding": self.model.encode(description).tolist()
        }
        self.knowledge.append(entry)
        
        # Update FAISS
        embeddings = np.array([e["embedding"] for e in self.knowledge])
        self.index = faiss.IndexFlatL2(384)
        self.index.add(embeddings.astype('float32'))
        faiss.write_index(self.index, 'data/kb_index.faiss')
        
        # Save JSON
        with open('data/kb.json', 'w') as f:
            json.dump(self.knowledge, f)
    
    def find_similar_tasks(self, description: str, top_k: int = 2) -> List[Dict]:
        """Find similar past tasks"""
        # Return empty list if knowledge base is empty
        if not self.knowledge or self.index.ntotal == 0:
            return []
        
        embedding = self.model.encode(description)
        distances, indices = self.index.search(np.array([embedding]).astype('float32'), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(self.knowledge):
                entry = self.knowledge[idx]
                results.append({
                    "task_id": entry["task_id"],
                    "similarity": float(1 - distances[0][i]/2) if distances[0][i] > 0 else 1.0,
                    "solution": entry["solution"]
                })
        return results

