import time
import json
import os
import pandas as pd
import streamlit as st
from runner import execute_prompt, run_single_eval

st.set_page_config(
    page_title="PromptCraft Matrix",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚡ PromptCraft Matrix: Prompt Evaluator Suite")
st.caption("Benchmark prompt variations using Groq models and structured LLM-as-a-Judge evaluation.")

st.sidebar.header("⚙️ Configuration")

dataset = []
if os.path.exists("test_dataset.json"):
    with open("test_dataset.json", "r") as f:
        dataset = json.load(f)

test_input = ""
if dataset:
    st.sidebar.subheader("🎯 Test Dataset")
    options = [f"[{item['category']}] {item['input'][:35]}..." for item in dataset]
    selected_idx = st.sidebar.selectbox("Choose a test case:", range(len(options)), format_func=lambda x: options[x])
    test_input = dataset[selected_idx]["input"]
else:
    st.sidebar.warning("`test_dataset.json` not found. Manual input required.")

user_input = st.text_area("User Test Input:", value=test_input, height=120)

st.markdown("---")

st.header("📝 Prompts Under Test")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Prompt A (Baseline)")
    prompt_a = st.text_area(
        "System Prompt A:",
        value="You are a helpful AI assistant. Answer the user prompt accurately.",
        height=150,
        key="prompt_a"
    )

with col2:
    st.subheader("Prompt B (Engineered)")
    prompt_b = st.text_area(
        "System Prompt B:",
        value="You are an expert assistant. Think step-by-step. Strictly follow all formatting, constraints, and instructions.",
        height=150,
        key="prompt_b"
    )

if st.button("🚀 Run Evaluation", type="primary", use_container_width=True):
    if not user_input.strip():
        st.error("Please provide a valid user test input!")
    else:
        with st.spinner("Executing models and running LLM Judge..."):
            
            start_a = time.perf_counter()
            output_a = execute_prompt(prompt_a, user_input)
            latency_a = time.perf_counter() - start_a
            eval_a = run_single_eval(user_input, prompt_a, output_a)

            start_b = time.perf_counter()
            output_b = execute_prompt(prompt_b, user_input)
            latency_b = time.perf_counter() - start_b
            eval_b = run_single_eval(user_input, prompt_b, output_b)

        st.markdown("---")
        st.header("🔍 Comparative Results")

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Prompt A Output")
            st.info(output_a)
            st.caption(f"⏱️ Latency: {latency_a:.2f} seconds")
            
            st.markdown("##### 📊 Judge Metrics")
            m1, m2, m3 = st.columns(3)
            m1.metric("Accuracy", f"{eval_a.accuracy_score}/5")
            m2.metric("Relevance", f"{eval_a.relevance_score}/5")
            m3.metric("Formatting", f"{eval_a.formatting_score}/5")
            
            with st.expander("Show Judge Chain-of-Thought"):
                st.write(eval_a.chain_of_thought)
                st.caption(f"**Verdict:** {eval_a.final_verdict}")

        with col_b:
            st.subheader("Prompt B Output")
            st.success(output_b)
            st.caption(f"⏱️ Latency: {latency_b:.2f} seconds")

            st.markdown("##### 📊 Judge Metrics")
            m1, m2, m3 = st.columns(3)
            m1.metric("Accuracy", f"{eval_b.accuracy_score}/5")
            m2.metric("Relevance", f"{eval_b.relevance_score}/5")
            m3.metric("Formatting", f"{eval_b.formatting_score}/5")

            with st.expander("Show Judge Chain-of-Thought"):
                st.write(eval_b.chain_of_thought)
                st.caption(f"**Verdict:** {eval_b.final_verdict}")

        st.markdown("---")
        st.header("📈 Overall Metrics Summary")

        summary_data = {
            "Prompt": ["Prompt A (Baseline)", "Prompt B (Engineered)"],
            "Accuracy (1-5)": [eval_a.accuracy_score, eval_b.accuracy_score],
            "Relevance (1-5)": [eval_a.relevance_score, eval_b.relevance_score],
            "Formatting (1-5)": [eval_a.formatting_score, eval_b.formatting_score],
            "Latency (s)": [round(latency_a, 2), round(latency_b, 2)]
        }

        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True)

        df_chart = df.set_index("Prompt")[["Accuracy (1-5)", "Relevance (1-5)", "Formatting (1-5)"]]
        st.bar_chart(df_chart)