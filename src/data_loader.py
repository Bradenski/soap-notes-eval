import json
from typing import Dict, List

def load_dataset(filepath: str = '../data/synthetic_data.json') -> List[Dict]:
    '''Load synthetic test dataset'''

    with open(filepath, 'r') as f: 
        data = json.load(f)
    return data