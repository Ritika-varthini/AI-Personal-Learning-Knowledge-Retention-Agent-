import os
import re
import json
from typing import Optional, Dict

# Configuration (Use environment variables)
HF_TOKEN = os.getenv("HF_TOKEN", "") # Add your token to environment variables
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"

def extract_json_robust(response_text: str) -> Optional[Dict]:
    """
    Multi-strategy JSON extraction from LLM output.
    Handles markdown code blocks, extra text, and nested structures.
    """
    # Strategy 1: Find JSON in markdown code blocks
    code_block_pattern = r'```(?:json)?\s*([\s\S]*?)```'
    matches = re.findall(code_block_pattern, response_text)
    if matches:
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue

    # Strategy 2: Find outermost JSON object braces
    try:
        start = response_text.find('{')
        end = response_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            json_str = response_text[start:end+1] # type: ignore
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    # Strategy 3: Line-by-line JSON detection (for multiline)
    lines = response_text.split('\n')
    json_buffer = []
    in_json = False
    brace_count = 0

    for line in lines:
        if '{' in line and not in_json:
            in_json = True
            json_buffer = []

        if in_json:
            json_buffer.append(line)
            brace_count += line.count('{') - line.count('}')

            if brace_count == 0 and '{' in ''.join(json_buffer):
                try:
                    return json.loads('\n'.join(json_buffer))
                except json.JSONDecodeError:
                    continue

    return None

def get_sentiment_emotion(notes: str):
    """Simple emotion detection based on keyword matching (low dependency)"""
    try:
        from textblob import TextBlob # type: ignore
        blob = TextBlob(notes)
        polarity = blob.sentiment.polarity
    except ImportError:
        return "Neutral/Focused"
    
    if polarity < -0.3:
        return "Stressed/Overwhelmed"
    elif polarity < -0.1:
        return "Uncertain/Anxious"
    elif polarity > 0.3:
        return "Confident/Excited"
    elif polarity > 0.1:
        return "Optimistic"
    else:
        return "Neutral/Focused"
