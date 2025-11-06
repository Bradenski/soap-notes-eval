import json
from typing import Dict, List
from pathlib import Path

# def load_dataset(filepath: str = '../data/synthetic_data.json') -> List[Dict]:
def load_dataset(filepath: str = None) -> List[Dict]:
    '''Load synthetic test dataset'''
    if filepath is None: 
        root = Path(__file__).parent.parent
        filepath = root / 'data' / 'synthetic_data.json'
    with open(filepath, 'r') as f: 
        data = json.load(f)
    return data