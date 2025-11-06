class ProductionQualityMonitor:
    """Monitor production notes for completeness based on SOAP standards based on guidelines and common words found here https://www.ncbi.nlm.nih.gov/books/NBK482263/"""
    
    def __init__(self):
        # Based on SOAP note standards
        self.required_elements = {
            'subjective': {
                'chief_complaint_indicators': ['presenting', 'reports', 'complains', 'chief complaint'],
                'hpi_indicators': ['duration', 'onset', 'started', 'began', 'history'],
                'temporal': ['days', 'weeks', 'months', 'years', 'ago']
            },
            'objective': {
                'vitals': ['bp', 'blood pressure', 'heart rate', 'hr', 'temperature', 'temp'],
                'physical_exam': ['exam', 'examination', 'appears', 'alert', 'oriented'],
                'findings': ['reveals', 'shows', 'noted', 'observed']
            },
            'assessment': {
                'diagnosis': ['diagnosis', 'diagnosed', 'assessment', 'likely', 'suggests', 'consistent with'],
                'differential': ['differential', 'possible', 'rule out', 'consider']
            },
            'plan': {
                'next_steps': ['order', 'prescribe', 'refer', 'follow up', 'schedule'],
                'medications': ['mg', 'medication', 'drug', 'dose'],
                'patient_education': ['educate', 'advise', 'instruct', 'counsel']
            }
        }
    
    def evaluate(self, note):
        """Check if note meets SOAP quality standards"""
        
        sections = self._extract_sections(note)
        issues = []
        scores = {}
        
        # Check each section
        for section_name, section_text in sections.items():
            if section_name in self.required_elements:
                score = self._check_section_quality(
                    section_text, 
                    self.required_elements[section_name]
                )
                scores[section_name] = score
                
                if score < 0.3:  # Less than 30% of expected elements
                    issues.append(f"{section_name.title()} section incomplete")
        
        overall_score = sum(scores.values()) / len(scores) if scores else 0
        
        return {
            'overall_quality_score': overall_score,
            'section_scores': scores,
            'issues': issues,
            'meets_standards': overall_score >= 0.5  # 50% threshold
        }
    
    def _check_section_quality(self, text, indicators_dict):
        """Check what % of expected indicators are present"""
        text_lower = text.lower()
        found_count = 0
        total_categories = len(indicators_dict)
        
        for category, keywords in indicators_dict.items():
            if any(kw in text_lower for kw in keywords):
                found_count += 1
        
        return found_count / total_categories if total_categories > 0 else 0
    
    def _extract_sections(self, note):
        """Extract SOAP sections from note"""
        import re
        
        sections = {}
        section_names = ['subjective', 'objective', 'assessment', 'plan']
        
        for section in section_names:
            pattern = rf'{section}:?\s*\n(.*?)(?=\n[A-Z][a-z]+:|\Z)'
            match = re.search(pattern, note, re.IGNORECASE | re.DOTALL)
            sections[section] = match.group(1).strip() if match else ""
        
        return sections