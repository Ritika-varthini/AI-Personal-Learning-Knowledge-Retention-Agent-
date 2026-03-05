import faiss
import numpy as np
from embeddings import get_embedding

# Sample learning resources database
resources = [
    "Complete OAuth Guide for Spring Boot",
    "JWT Authentication Tutorial",
    "React Beginner to Advanced Course",
    "Docker for Developers",
    "DevOps CI/CD Pipeline Explained",
    "Spring Boot REST API Development",
    "Node.js API Development Masterclass",
    "Database Design Fundamentals"
]

# Create embeddings for resources
resource_embeddings = np.array(
    [get_embedding(text) for text in resources]
).astype("float32")

dimension = resource_embeddings.shape[1]

# Build FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(resource_embeddings)


def recommend_resources(query: str, top_k: int = 3):
    query_vector = np.array([get_embedding(query)]).astype("float32")

    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        results.append(resources[idx])

    return results