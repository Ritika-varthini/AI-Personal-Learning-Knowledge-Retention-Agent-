from skill_gap_module.task_processor import process_single_task
from knowlege_base.kb_manager import KnowledgeBase
from motivation_module.motivator import Motivator

class UnifiedTaskProcessor:
    def __init__(self):
        self.kb = KnowledgeBase()
        self.motivator = Motivator()
    
    def process_complete_task(self, task_id: str, description: str, notes: str) -> dict:
        """🚀 COMPLETE PIPELINE: All 3 modules unified"""
        
        # 1️⃣ Skill Gap Detection (Member 1)
        skill_result = process_single_task(task_id, description, notes)
        
        # 2️⃣ Knowledge Base Check (Member 2)
        similar_tasks = self.kb.find_similar_tasks(description)
        
        # 3️⃣ Motivation Generation (Member 3)
        emotion = skill_result["emotion_detected"]
        skill_gap = skill_result["detected_skill_gaps"][0] if skill_result["detected_skill_gaps"] else "core skills"
        motivation = self.motivator.generate_motivational_story(emotion, skill_gap)
        
        # 🎯 FINAL COMBINED RESULT
        final_result = {
            **skill_result,
            "knowledge_base": {
                "similar_tasks_found": len(similar_tasks) > 0,
                "similar_tasks": similar_tasks
            },
            "motivation": motivation,
            "system_status": "All modules integrated successfully ✅"
        }
        
        return final_result

