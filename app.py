import json
import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from nlp_module.skill_detection import detect_skill_gap, get_learning_resources, generate_motivation # type: ignore
    from kb_module.knowledge_base import store_knowledge, retrieve_knowledge # type: ignore
    from utils.helpers import get_sentiment_emotion # type: ignore
except ImportError:
    pass

def run_pipeline(task_description: str, employee_notes: str = ""):
    """
    Unified Pipeline:
    User Input → NLP Processing → Skill Detection → Knowledge Retrieval → Story/Motivation → UI Output
    """
    from utils.helpers import HF_TOKEN # type: ignore
    
    status = "Success ✅"
    if not HF_TOKEN or HF_TOKEN == "":
        status = "Warning ⚠️: HF_TOKEN missing in environment. Using fallback logic."
    
    # 1. EMOTION ANALYSIS (NLP Processing)
    emotion = get_sentiment_emotion(employee_notes)
    
    # 2. SKILL DETECTION (NLP Module)
    # Using separate task and notes for better expert mentor context
    skill_gaps = detect_skill_gap(task_description, employee_notes)
    
    # 3. KNOWLEDGE RETRIEVAL (KB Module)
    # Check if we have similar tasks already solved
    past_solutions = retrieve_knowledge(task_description)
    
    # 4. GET LEARNING RESOURCES (GPT-based suggestions)
    # Now returns a list of resource dicts
    resources = get_learning_resources(skill_gaps)
        
    # 5. MOTIVATION & STORY (NLP Logic)
    context = f"Learning {', '.join(skill_gaps)}"
    motivation = generate_motivation(emotion, context)
    
    # 6. RETURN COMPLETE OUTPUT
    return {
        "status": status,
        "task": task_description,
        "emotion": emotion,
        "skill_gaps": skill_gaps,
        "resources": [
            {
                "skill": res["skill"],
                "tutorial": res["tutorial"],
                "code": res.get("code_snippet", "# No code available"),
                "link": res.get("resource_link", "#")
            } for res in resources
        ],
        "past_learning": past_solutions,
        "motivation_quote": motivation.get('quote', 'Keep pushing forward!'),
        "motivation_tip": motivation.get('tip', 'Every small step counts.')
    }

if __name__ == "__main__":
    # Test case for command-line validation
    sample_task = "Build a REST API with Flask and SQLAlchemy."
    sample_notes = "I'm struggling with the db configurations."
    
    print("\n🚀 --- AI-LKRA SYSTEM TEST ---")
    result = run_pipeline(sample_task, sample_notes)
    print(json.dumps(result, indent=2))
    
    # Optional: Save back to KB for future
    store_knowledge(sample_task, "Set up SQLAlchemy app factory and SQLALCHEMY_DATABASE_URI in config.")
    print("\n✅ System integration test complete!")
