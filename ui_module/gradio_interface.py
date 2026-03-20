import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import gradio as gr # type: ignore
    from app import run_pipeline # type: ignore
    from kb_module.knowledge_base import store_knowledge # type: ignore
except ImportError:
    pass

def process_task(task_desc, notes):
    """Gradio-friendly wrapper for the pipeline"""
    if not task_desc or not notes:
        return {"error": "Provide both task and notes"}
    
    # Run pipeline
    results = run_pipeline(task_desc, notes)
    
    # Format for JSON output
    return results

def save_to_kb(task, solution):
    """Gradio-friendly KB saving"""
    if task and solution:
        store_knowledge(task, solution)
        return "✅ Saved to Knowledge Base!"
    return "❌ Error: Fill both task and solution."

# 🎨 Gradio Theme and Layout
with gr.Blocks(title="AI-LKRA: AI Learning Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 AI Personal Learning & Knowledge Retention Agent (AI-LKRA)")
    gr.Markdown("#### Unified Module Demo: NLP + KB + UI")
    
    with gr.Row():
        with gr.Column(scale=1):
            task_in = gr.Textbox(label="📋 Task Description", lines=4, placeholder="Describe the technical task...")
            notes_in = gr.Textbox(label="😰 Employee Notes", lines=3, placeholder="What's confusing or difficult?")
            analyze_btn = gr.Button("🔍 Analyze Skill Gaps", variant="primary")
            
        with gr.Column(scale=2):
            output_json = gr.JSON(label="📊 Pipeline Output (Unified Results)", height=500)
    
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 💾 Save to Knowledge Base")
            kb_task = gr.Textbox(label="Task Name", placeholder="e.g., Flask Blueprint setup")
            kb_sol = gr.Textbox(label="Learning/Solution", placeholder="e.g., Use Blueprint(...) and register with app.register_blueprint(...)")
            save_btn = gr.Button("Save to KB")
            save_msg = gr.Label(value="")

    # Connections
    analyze_btn.click(fn=process_task, inputs=[task_in, notes_in], outputs=output_json)
    save_btn.click(fn=save_to_kb, inputs=[kb_task, kb_sol], outputs=save_msg)

if __name__ == "__main__":
    demo.launch(share=False)
