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

def detect_skill_gap(input_text: str) -> List[str]:
    """
    Identifies 2-3 technical skill gaps from the provided text.
    Handles both task and notes combined in input_text.
    """
    truncated_text = str(input_text)[:700] # type: ignore
    prompt = f"""<s>[INST] Identity 2-3 SPECIFIC technical skill gaps based on this text:
{truncated_text}

OUTPUT FORMAT (STRICT JSON):
{{ "skill_gaps": ["specific concept 1", "specific concept 2"] }}
[/INST]</s>"""

    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=200,
            temperature=0.1
        )
        parsed = extract_json_robust(response)
        if parsed and "skill_gaps" in parsed:
            # Filter for specific skills (more than 2 words)
            gaps = [g for g in parsed["skill_gaps"] if len(g.split()) >= 1]
            final_gaps = list(gaps)[:3] # type: ignore
            return final_gaps
    except Exception as e:
        print(f"Skill detection error: {e}")
    
    # Simple Fallback
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
