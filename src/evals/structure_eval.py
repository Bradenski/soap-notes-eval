import re 

SECTIONS = ['Subjective', 'Objective', 'Assessment', 'Plan']
    
def structure_eval(generated_note: str) -> dict[str, any]:
    """Evaluate generated SOAP note structure"""
    results = {
        'has_all_sections': True,
        'sections': {},
        'total_words': len(generated_note.split()),
        'total_chars': len(generated_note),
        'flags': []
    }
    
    for section in SECTIONS:
        # Check if section exists
        pattern = rf'{section}:?\s*\n(.*?)(?=\n[A-Z][a-z]+:|\Z)'
        match = re.search(pattern, generated_note, re.IGNORECASE | re.DOTALL)
        
        if not match:
            results['has_all_sections'] = False
            results['sections'][section] = {
                'present': False,
                'word_count': 0,
                'char_count': 0
            }
            results['flags'].append(f"Missing section: {section}")
        else:
            content = match.group(1).strip()
            word_count = len(content.split())
            char_count = len(content)
            
            results['sections'][section] = {
                'present': True,
                'word_count': word_count,
                'char_count': char_count
            }
            
            # Flag if empty or very short
            if word_count == 0:
                results['flags'].append(f"Empty section: {section}")
            elif word_count < 10:
                results['flags'].append(f"Very short section: {section} ({word_count} words)")
    
    return results