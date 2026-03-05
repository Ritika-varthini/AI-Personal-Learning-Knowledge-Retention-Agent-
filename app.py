from fastapi import FastAPI, Query
from skill_detector import detect_skills
from resource_generator import recommend_resources
from memory_store import save_to_memory, get_memory

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Learning Engine Running 🚀"}


# Phase 1 - Skill Detection
@app.get("/detect")
def detect(task: str = Query(...)):
    result = detect_skills(task)
    save_to_memory({"task": task, "detection": result})
    return result


# Phase 2 - Resource Recommendation
@app.get("/recommend")
def recommend(task: str = Query(...)):
    resources = recommend_resources(task)
    save_to_memory({"task": task, "resources": resources})
    return {"recommended_resources": resources}


# Memory endpoint
@app.get("/memory")
def memory():
    return get_memory()