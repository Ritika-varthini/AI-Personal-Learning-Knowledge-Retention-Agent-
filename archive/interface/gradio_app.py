import gradio as gr
from skill_gap_module.enhanced_processor import UnifiedTaskProcessor

processor = UnifiedTaskProcessor()

def process_task(task_desc, notes):
    return processor.process_complete_task("DEMO_TASK", task_desc, notes)

interface = gr.Interface(
    fn=process_task,
    inputs=[
        gr.Textbox(label="📋 Task Description", lines=4),
        gr.Textbox(label="😰 Employee Notes", lines=2)
    ],
    outputs=gr.JSON(label="🚀 Complete Analysis", height=600),
    title="🤖 AI Learning Agent - All 3 Modules Integrated",
    description="Skill Gap Detection + Knowledge Base + Motivation Generator"
)

