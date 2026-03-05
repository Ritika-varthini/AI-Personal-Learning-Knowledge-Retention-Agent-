from transformers import pipeline

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

SKILL_LABELS = [
    "JWT",
    "OAuth",
    "Node.js",
    "Spring Boot",
    "Docker",
    "DevOps",
    "React",
    "Database",
    "Authentication",
    "API Development"
]

def detect_skills(task_text: str):
    result = classifier(task_text, SKILL_LABELS)

    top_skills = result["labels"][:2]

    # Domain logic
    if "React" in top_skills:
        domain = "Frontend"
    elif "DevOps" in top_skills or "Docker" in top_skills:
        domain = "DevOps"
    else:
        domain = "Backend"

    # Difficulty logic
    if "OAuth" in top_skills or "JWT" in top_skills:
        difficulty = "Intermediate"
    elif "Docker" in top_skills:
        difficulty = "Advanced"
    else:
        difficulty = "Beginner"

    return {
        "skills_detected": top_skills,
        "domain": domain,
        "difficulty_estimate": difficulty
    }