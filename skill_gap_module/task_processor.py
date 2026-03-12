from huggingface_hub import InferenceClient
from config.config import HF_TOKEN, MODEL_NAME
from textblob import TextBlob
from datetime import datetime
import json

client = InferenceClient(MODEL_NAME, token=HF_TOKEN)

def detect_skill_gaps_llm(description, notes):
    prompt = f"""
<s>[INST]You are a senior software architect. Identify 1-2 HIGHLY SPECIFIC technical skill gaps from:
Task: {description[:250]}
Notes: "{notes}"
Return ONLY valid JSON: {{"skill_gaps": ["specific skill 1", "specific skill 2"]}}[/INST]</s>
"""
    try:
        response = client.text_generation(prompt, max_new_tokens=150, temperature=0.05)
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != -1:
            parsed = json.loads(response[start:end])
            gaps = parsed.get("skill_gaps", [])
            filtered = [g for g in gaps if len(g.split()) > 2]
            return filtered[:2] if filtered else ["React useEffect lifecycle"]
    except:
        pass
    return ["React useEffect lifecycle"]

def process_single_task(task_id, description, notes):
    # Emotion
    polarity = TextBlob(notes).sentiment.polarity
    emotion = "Stressed" if polarity < -0.1 else "Happy" if polarity > 0.1 else "Neutral"
    
    # Skill gaps
    skill_gaps = detect_skill_gaps_llm(description, notes)
    
    return {
        "task_id": task_id,
        "emotion_detected": emotion,
        "detected_skill_gaps": skill_gaps,
        "timestamp": datetime.now().isoformat()
    }

