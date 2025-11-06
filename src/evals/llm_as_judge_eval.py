import anthropic 

class LLMAsJudgeEval:
    """Use LLM as Judge to detect inaccuracies and halucinations in generated SOAP notes"""
    
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def evaluate(self, transcript: str, generated_note: str):
        """Check if generated SOAP note is missing critical findings, contains hallucinatinos, or has clinical inaccuracies compared to original transcript"""
        
        prompt = f"""You are evaluating a medical SOAP note for clinical accuracy based on the provided transcript of the patient conversation.

TRANSCRIPT (what was actually said):
{transcript}

GENERATED NOTE:
{generated_note}

Task: 
1. Identify HALLUCINATIONS - facts in the note NOT supported by the transcript
2. Identify CLINICAL INACCURACIES - medically incorrect statements (wrong dosages, contraindications, inappropriate treatments)
3. Identify MISSING FINDINGS - important facts from the transcript that are absent from the note

Be specific and cite examples.

Format your response as:
HALLUCINATIONS: [list each hallucinated fact, or "None detected"]
CLINICAL INACURACIES: [list each innacuracy, or "None detected"]
MISSING FINDINGS: [list each missing critical finding, or "None detected"]
CONFIDENCE: [High/Medium/Low]
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result_text = response.content[0].text
        
        # Simple parsing
        has_hallucinations = "None detected" not in result_text
        has_clinical_inaccuracies = "None detected" not in result_text
        has_missing_findings = "None detected" not in result_text
        
        return {
            'has_hallucinations': has_hallucinations,
            'has_clinical_inaccuracies': has_clinical_inaccuracies,
            'has_missing_findings': has_missing_findings,
            'llm_response': result_text
        }