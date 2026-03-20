#!/usr/bin/env python3
"""
🚀 COMPLETE AI LEARNING AGENT - Production Ready
"""
from skill_gap_module.enhanced_processor import UnifiedTaskProcessor
import json

def demo():
    processor = UnifiedTaskProcessor()
    
    # Test the complete system
    result = processor.process_complete_task(
        "TEST_001",
        "Build React dashboard with WebSocket real-time data",
        "I don't understand useEffect and state management with hooks"
    )
    
    print("🎉 COMPLETE SYSTEM TEST:")
    print(json.dumps(result, indent=2))
    
    # Save first lesson to KB (demo)
    processor.kb.save_lesson("TEST_001", "Build React dashboard with WebSocket real-time data", "Completed with useEffect tutorial")
    print("\n✅ Lesson saved to Knowledge Base!")

if __name__ == "__main__":
    # Test CLI
    demo()
    
    # Launch UI
    from interface.gradio_app import interface
    interface.launch(share=False)
