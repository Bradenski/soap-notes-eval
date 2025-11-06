from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(generated_note: str, ground_truth_note: str) -> tuple[float,str]:
    '''Calculate semantic similarity between GT and generated SOAP notes using SBERT'''

    embeddings = model.encode([generated_note, ground_truth_note])
    similarity = model.similarity(embeddings[0], embeddings[1]).item()
    quality = "null"
    if similarity >= 0.85:
        quality = "EXCELLENT"  # Minor differences only
    elif similarity >= 0.75:
        quality = "GOOD"  # Acceptable, may have minor omissions
    elif similarity >= 0.65:
        quality = "NEEDS REVIEW"  # Significant differences
    else:
        quality = "POOR"
    return round(similarity, 3), quality
    