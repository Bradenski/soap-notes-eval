import streamlit as st 
from data_loader import load_dataset
from evals.similarity_eval import calculate_similarity
from evals.llm_as_judge_eval import LLMAsJudgeEval
from evals.structure_eval import structure_eval
from evals.clinical_completeness_eval import ProductionQualityMonitor
import os 

# Load our synthetic dataset to simulate evals
test_data = load_dataset()

st.title("SOAP Note Eval Dashboard")

# Several patients scenarios have been designed for exploring metrics  
case_id = st.selectbox("Select patient:", options=[case['id'] for case in test_data])
selected_case = test_data[case_id]

# Show original transcript 
st.subheader("Transcript")
st.write('Patient label: ' + selected_case['label']) 

transcript = selected_case['transcript']
st.text_area("", value=transcript, height=300, key='transcript')

# Show generated SOAP note on left, ground truth SOAP note on right
gen_col, gt_col = st.columns(2)
with gen_col: 
    st.subheader("Generated SOAP Note")
    st.text_area("", selected_case["generated_soap"], height=400, key='gen_col')

with gt_col: 
    st.subheader("Ground Truth")
    st.text_area("", selected_case["gt_soap"], height=400, key='gt_col')


# Structural eval to check some basic things, like if all SOAP sections exist and word and char count
st.subheader("Structural Evaluation")
structure_results = structure_eval(selected_case['generated_soap'])
all_sections, total_words, total_chars = st.columns(3)
all_sections.metric("Has All Sections", structure_results['has_all_sections'])
total_words.metric("Word Count", structure_results['total_words'])
total_chars.metric("Char Count", structure_results['total_chars'])
st.text(f"Flags: {structure_results['flags']}")

# Similarity score between generated SOAP note and its ground truth
st.subheader('Similarity via SBERT')
similarity_score = calculate_similarity(selected_case['generated_soap'], selected_case['gt_soap'])
similarity = f'Quality: {similarity_score[1]}, Similarity Score: {similarity_score[0]}'

# Colors indicate similarity quality 
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

# LLM as Judge to evaluate SOAP note quality 
# load API key localally with dotenv or from Streamlit secrets
try: 
    api_key = st.secrets['ANTHROPIC_API_KEY']
    st.success('Loaded api key from secrets!', icon="✅")
except: 
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('ANTHROPIC_API_KEY')

run_llm_eval = LLMAsJudgeEval(api_key=api_key)

if st.button("Run LLM as Judge Eval"): 
    result = run_llm_eval.evaluate(transcript=selected_case['transcript'], generated_note=selected_case['generated_soap'])
    col1, col2, col3 = st.columns(3)
    col1.metric("Has Hallucinations", result['has_hallucinations'])
    col2.metric("Has Clinical Inaccuracies", result['has_clinical_inaccuracies'])
    col3.metric("Has Missing Findings", result['has_missing_findings'])
    st.write(result['llm_response'])

# Experimental: clincial completeness, would benefit from refinement with SME 
st.subheader("Clinical Completeness Score")
completeness_eval = ProductionQualityMonitor()
quality = completeness_eval.evaluate(selected_case['generated_soap'])
st.write(f"**Score: {quality['overall_quality_score']:1%}**")
if quality['overall_quality_score'] < 0.3:
    st.error("⚠️ Note may be incomplete - missing key clinical elements")
elif quality['overall_quality_score'] < 0.5:
    st.warning("⚠️ Note could be more complete")
else:
    st.success("✅ Note meets minimum standards")