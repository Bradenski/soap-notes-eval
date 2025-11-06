import streamlit as st 
from data_loader import load_dataset
from evals.similarity_eval import calculate_similarity
from evals.llm_as_judge_eval import LLMAsJudgeEval
from evals.structure_eval import structure_eval
import os 
from dotenv import load_dotenv

load_dotenv()

test_data = load_dataset()

st.title("SOAP Note Eval Dashboard")

case_id = st.selectbox("Select patient:", options=[case['id'] for case in test_data])
selected_case = test_data[case_id]

st.subheader("Transcript")
st.write('Patient label: ' + selected_case['label']) 

transcript = selected_case['transcript']
st.text_area("", value=transcript, height=300)

st.subheader("Structural Evaluation")

structure_results = structure_eval(selected_case['generated_soap'])
all_sections, total_words, total_chars = st.columns(3)
all_sections.metric("Has All Sections", structure_results['has_all_sections'])
total_words.metric("Word Count", structure_results['total_words'])
total_chars.metric("Char Count", structure_results['total_chars'])
st.text(f"Flags: {structure_results['flags']}")

st.subheader('Similarity via SBERT')
similarity_score = calculate_similarity(selected_case['generated_soap'], selected_case['gt_soap'])
similarity = f'Quality: {similarity_score[1]}, Similarity Score: {similarity_score[0]}'
# color to indicate similarity quality 
quality_colors = {
    'EXCELLENT': 'green',
    'GOOD': 'green', 
    'NEEDS REVIEW': 'orange', 
    'POOR': 'red'
    }
st.markdown(
    f"<span style='color:{quality_colors[similarity_score[1]]}; font-weight:bold; font-size: large;'>{similarity_score[1]}</span><br>"
    f"Similarity score: {similarity_score[0]}",
    unsafe_allow_html=True
    )

run_llm_eval = LLMAsJudgeEval(api_key=os.getenv('ANTHROPIC_API_KEY'))

if st.button("Run LLM as Judge Eval"): 
    result = run_llm_eval.evaluate(transcript=selected_case['transcript'], generated_note=selected_case['generated_soap'])
    col1, col2, col3 = st.columns(3)
    col1.metric("Has Hallucinations", result['has_hallucinations'])
    col2.metric("Has Clinical Inaccuracies", result['has_clinical_inaccuracies'])
    col3.metric("Has Missing Findings", result['has_missing_findings'])
    st.write(result['llm_response'])


