import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

from utils.dictToString import dict_to_string

# Inicializar o modelo BERT para a classificação
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_embedding(text: str):
    """Obtém o embedding de um texto usando BERT."""

    try:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        output = outputs.last_hidden_state[:, 0, :].numpy()
        return output
    except Exception as e:
        print(f"Erro get_embedding: {e}")
        return None

def classify_issue(issue: dict, threshold: float = 0.75) -> list:
    """
    Classifica a issue como 'Refatoração', 'Testes de Regressão', ambas ou nenhuma,
    com base na similaridade do cosseno.
    
    Args:
        issue (dict): Dicionário contendo os dados da issue.
        threshold (float): Limiar de similaridade para considerar uma classificação válida.
                          Padrão é 0.75.
    
    Returns:
        list: Lista de classificações ('Refatoração', 'Testes de Regressão' ou vazia).
    """

    issue_text = dict_to_string(issue)
    issue_embedding = get_embedding(issue_text)
    
    refactor_examples = [
        "Code improvement", "Function refactoring", "Performance optimization",
        "Reducing code duplication", "Improving code readability",
        "Applying design patterns", "Modularizing functions",
        "Rewriting complex logic", "Optimizing database queries",
        "Upgrading dependencies for maintainability"
    ]

    regression_test_examples = [
        "Fix bug", "Failed after change", "Error in existing functionality",
        "Unexpected behavior after update", "Feature stopped working",
        "Regression detected in production", "Rolling back due to failure",
        "Unit tests failing after commit", "Fixing broken API response",
        "Resolving UI glitch introduced by refactor"
    ]
    
    refactor_embedding = get_embedding(" ".join(refactor_examples))
    regression_embedding = get_embedding(" ".join(regression_test_examples))
    
    try :
        similarity_refactor = cosine_similarity(issue_embedding, refactor_embedding)[0][0]
        similarity_regression = cosine_similarity(issue_embedding, regression_embedding)[0][0]
        
        classifications = []
        if similarity_refactor >= threshold:
            classifications.append("Refatoracao")
        if similarity_regression >= threshold:
            classifications.append("Testes de Regressao")
    except Exception as e:
        print(f"Erro classify_issue: {e}")

    return classifications