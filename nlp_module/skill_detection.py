import os
import sys
from typing import List, Dict, Optional

# Add root to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from huggingface_hub import InferenceClient # type: ignore
    from utils.helpers import HF_TOKEN, MODEL_NAME, extract_json_robust, get_sentiment_emotion # type: ignore
except ImportError:
    # This might happen during linting if dependencies aren't installed
    pass

# Initialize HuggingFace client
client = InferenceClient(MODEL_NAME, token=HF_TOKEN)

def detect_skill_gap(task: str, notes: str) -> List[str]:
    """
    Identifies specific technical skill gaps using an expert mentor persona.
    """
    task_trunc = str(task)[:500] # type: ignore
    notes_trunc = str(notes)[:400] # type: ignore
    
    prompt = f"""<s>[INST] You are an expert software engineering mentor and AI system.
Your task is to analyze a user's task description and struggles, and identify SPECIFIC technical skill gaps.

DO NOT give generic answers.

INPUT:
Task Description: {task_trunc}
Struggles / Notes: {notes_trunc}

RULES:
1. Extract EXACT technologies, tools, and concepts mentioned or implied.
2. Identify REAL skill gaps based on missing knowledge.
3. Be SPECIFIC and CONCRETE (e.g., 'Flask routing' instead of 'API').
4. Use both task and struggles context.
5. If user says 'I don't know X', include X as a skill gap.

OUTPUT FORMAT (STRICT JSON):
{{
  "skill_gaps": ["Specific Skill 1", "Specific Skill 2"],
  "learning_suggestions": ["Suggestion 1", "Suggestion 2"]
}}
[/INST]</s>"""

    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=250,
            temperature=0.1
        )
        parsed = extract_json_robust(response)
        if parsed and "skill_gaps" in parsed:
            return list(parsed["skill_gaps"])[:4] # type: ignore
    except Exception as e:
        print(f"Skill detection error: {e}")
    
    return ["Task implementation patterns", "Relevant API documentation"]

def get_learning_resources(skills: List[str]) -> List[Dict]:
    """
    Generates tutorials and resources for a list of skills.
    """
    all_resources = []
    for skill in skills:
        prompt = f"""<s>[INST] Create a learning resource for this skill: {skill}

OUTPUT FORMAT (STRICT JSON):
{{
  "tutorial": "2-3 sentence explanation...",
  "code_snippet": "python_or_javascript_code...",
  "resource_link": "https://official-docs-url"
}}
[/INST]</s>"""

        try:
            response = client.text_generation(prompt, max_new_tokens=400, temperature=0.2)
            parsed = extract_json_robust(response)
            if parsed and all(k in parsed for k in ["tutorial", "code_snippet", "resource_link"]):
                parsed["skill"] = skill
                all_resources.append(parsed)
        except Exception as e:
            print(f"Tutorial generation error for {skill}: {e}")
            all_resources.append({
                "skill": skill,
                "tutorial": f"Research {skill} in official docs.",
                "code_snippet": "# No code available",
                "resource_link": "https://developer.mozilla.org/en-US/"
            })
    return all_resources

def generate_motivation(emotion: str, context: str) -> Dict:
    """
    Generates a motivational story based on the detected emotion and task context.
    """
    prompt = f"""<s>[INST] Act as a career coach. Generate a motivational quote and tip.
USER EMOTION: {emotion}
TASK CONTEXT: {context}

OUTPUT FORMAT (STRICT JSON):
{{
  "quote": "Small progress is still progress...",
  "tip": "Focus on 15 mins of learning today."
}}
[/INST]</s>"""

    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=200,
            temperature=0.4
        )
        parsed = extract_json_robust(response)
        if parsed and "quote" in parsed:
            return parsed
    except:
        pass

    return {
        "quote": "Success is the sum of small efforts repeated daily.",
        "tip": "Break the task into smaller sub-tasks."
    }
