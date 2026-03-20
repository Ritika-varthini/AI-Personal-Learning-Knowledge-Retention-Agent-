from typing import Dict

class Motivator:
    def generate_motivational_story(self, emotion: str, skill_gap: str) -> Dict:
        """Generate motivation based on emotion + skill"""
        stories = {
            "Stressed": f"Once a dev was stuck on {skill_gap} too. They spent 15 mins daily on docs. Now they own it! 💪",
            "Neutral": f"Mastering {skill_gap} is your next power move. Small daily practice = big wins.",
            "Happy": f"You're already great! Add {skill_gap} mastery to become unstoppable. 🚀"
        }
        
        tips = {
            "Stressed": "Take 1 small step today - read 1 doc page.",
            "Neutral": "Practice 15 mins daily on LeetCode/HackerRank.",
            "Happy": "Teach {skill_gap} to someone else today!"
        }
        
        return {
            "story": stories.get(emotion, stories["Neutral"]),
            "tip": tips.get(emotion, tips["Neutral"]),
            "confidence": 0.9
        }

