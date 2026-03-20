import sys
import os

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import streamlit as st # type: ignore
    import json
    import time
    from app import run_pipeline # type: ignore
    from kb_module.knowledge_base import store_knowledge, retrieve_knowledge # type: ignore
except ImportError:
    pass

def launch_streamlit():
    """Builds a premium Streamlit UI for the AI Learning agent."""
    
    # 🎨 UI Configuration
    st.set_page_config(
        page_title="AI-LKRA: Personal Learning Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 🖌️ Custom Styling
    st.markdown("""
        <style>
            .main { background: #f8f9fa; }
            .stButton>button { 
                background: linear-gradient(135deg, #6c63ff, #4c44f0); 
                color: white; border-radius: 20px; border: none; padding: 10px 40px;
                font-weight: bold; width: 100%; transition: all 0.3s cubic-bezier(0, 0, 0.2, 1);
            }
            .stButton>button:hover { 
                transform: translateY(-2px); box-shadow: 0 5px 15px rgba(108, 99, 255, 0.4); 
            }
            .card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
            .badge { background: #eef2ff; color: #4338ca; padding: 4px 12px; border-radius: 999px; font-weight: 500; font-size: 0.85rem; border: 1px solid #c7d2fe; }
            .quote { font-style: italic; color: #4b5563; font-size: 1.1rem; border-left: 4px solid #6c63ff; padding-left: 15px; margin: 15px 0; }
        </style>
    """, unsafe_allow_html=True)

    # 🏰 Main Layout
    st.title("🎯 AI Personal Learning & Knowledge Retention Agent")
    st.caption("Empowering employees through automated skill gap detection and contextual learning.")

    with st.sidebar:
        st.header("⚙️ System Status")
        st.success("NLP Module: Loaded")
        st.success("KB Module: Ready")
        st.success("UI Module: Active")
        
        st.divider()
        st.subheader("💡 Tips for Best Results")
        st.info("Be specific in your task description and honest in your notes for accurate skill detection.")

    # 📥 INPUT SECTION
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 New Task Details")
        task_input = st.text_area(
            "What task are you working on?", 
            placeholder="e.g., Integrate a payment gateway using Stripe API in a Django app.",
            key="task_desc",
            height=150
        )
    
    with col2:
        st.subheader("😰 Struggles & Notes")
        notes_input = st.text_area(
            "What parts are unclear or difficult?",
            placeholder="e.g., I don't know how to handle webhooks and secret signing.",
            key="emp_notes",
            height=150
        )

    btn_clicked = st.button("🔍 ANALYZE MY SKILL GAPS")

    if btn_clicked:
        if not task_input.strip() or not notes_input.strip():
            st.warning("⚠️ Please provide both a task and some notes so I can help!")
        else:
            with st.spinner("🚀 Analyzing your input with Mistral-7B..."):
                # Run the unified pipeline
                try:
                    results = run_pipeline(task_input, notes_input)
                    time.sleep(1) # For a small 'thinking' effect
                    
                    st.divider()
                    
                    # 📊 OUTPUT SECTION
                    res_col1, res_col2 = st.columns([1, 1])
                    
                    with res_col1:
                        st.subheader("🔍 Analysis Results")
                        st.write(f"**Detected Emotion:** {results['emotion']}")
                        
                        st.write("**Detected Skill Gaps:**")
                        for gap in results['skill_gaps']:
                            st.markdown(f"<span class='badge'>{gap}</span>", unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.write("### 📖 Learning Resources")
                        for res in results['resources']:
                            with st.expander(f"📚 Learn {res['skill']}"):
                                st.write(f"**Tutorial:** {res['tutorial']}")
                                if res['code'] and res['code'] != "# No specific snippet available":
                                    st.code(res['code'], language='python')
                                st.markdown(f"🔗 [Official Documentation]({res['link']})")

                    with res_col2:
                        st.subheader("🧠 Knowledge Base (Past Learnings)")
                        past = results['past_learning']
                        if past:
                            for p in past:
                                st.markdown(f"""
                                    <div class="card">
                                        <b>💡 Similar Past Task:</b><br/>{p['task']}<br/><br/>
                                        <b>🛠️ Past Solution:</b><br/>{p['solution']}
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("🧐 No similar tasks found in your Knowledge Base yet. Keep learning!")

                        st.subheader("✨ Final-Year Motivation")
                        st.markdown(f"<div class='quote'>\"{results['motivation_quote']}\"</div>", unsafe_allow_html=True)
                        st.success(f"**Pro-Tip:** {results['motivation_tip']}")

                except Exception as e:
                    st.error(f"❌ System error during processing: {str(e)}")

    # 📝 SAVE TO KB (MANUAL)
    with st.expander("💾 Save New Solution to Knowledge Base"):
        save_task = st.text_input("Task Name for KB", key="save_task")
        save_sol = st.text_area("What was the solution/learning?", key="save_sol")
        if st.button("Save to Knowledge Base"):
            if save_task and save_sol:
                store_knowledge(save_task, save_sol)
                st.toast("✅ Saved to Knowledge Base!")
            else:
                st.warning("Fill both fields to save.")

if __name__ == "__main__":
    launch_streamlit()
