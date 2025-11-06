# SOAP Notes Eval Suite

Evaluation framework for assessing the quality of AI-generated SOAP notes. A Streamlit dashboard showcases several approaches for detecting missing critical findings, hallucinated or unsupported facts, and clinical accuracy issues. 

[View Live Dashboard](https://soap-notes-eval.streamlit.app/)

Synthetic dataset built from [Soap Notes](https://huggingface.co/datasets/adesouza1/soap_notes).

## Evaluation Approaches

### 1. Structure Evaluator (Deterministic)
- **Speed:** <1ms per note
- **Cost:** Free
- **Purpose:** Validates SOAP section presence and completeness
- **Use Case:** Fast CI/CD checks, immediate feedback

### 2. Semantic Similarity (Reference-Based)
- **Speed:** ~500ms per note
- **Cost:** Local compute with embedding model
- **Purpose:** Measures similarity with ground truth notes
- **Use Case:** Benchmarking model performance

### 3. LLM-as-Judge (Comprehensive)
- **Speed:** Up to 5s per note
- **Cost:** $$$
- **Purpose:** Detects hallucinations, clinical inaccuracies, missing findings
- **Use Case:** Reference-free evaluation for live quality audit

### 4. Clinical Completeness Monitor (Production)
- **Speed:** <1ms per note
- **Cost:** Free
- **Purpose:** Checks adherence to SOAP documentation standards
- **Use Case:** Drift detection in production


## Setup
1. cd soap-notes-eval
2. Add your Anthropic API key to `.env`
3. pip install -r requirements.txt
4. streamlit run src/dashboard.py