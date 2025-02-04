import requests
import time
from datetime import datetime

def get_first_timeline_author(issue: dict, token: str = None) -> str:
    """
    Função que busca o autor da primeira ação realizada na timeline em uma issue.
    
    Args:
        issue (dict): Dicionário contendo os dados da issue.
        token (str): Token de autenticação do GitHub (opcional).
    
    Returns:
        str: Login do autor da primeira ação na timeline.
    """
    if 'timeline_url' not in issue or not issue['timeline_url']:
        return None

    timeline_link = issue['timeline_url']
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        timeline_response = requests.get(timeline_link, headers=headers)
        
        if timeline_response.status_code == 403 and "rate limit exceeded" in timeline_response.text:
            reset_time = int(timeline_response.headers.get("X-RateLimit-Reset"))
            sleep_time = reset_time - int(datetime.now().timestamp())
            print(f"Rate limit excedido. Esperando {sleep_time} segundos...")
            time.sleep(max(sleep_time, 1))  
            return get_first_timeline_author(issue, token)  
        
        if timeline_response.status_code == 200:
            timeline = timeline_response.json()
            
            if timeline:  
                first_action = timeline[0]
                if 'actor' in first_action and 'login' in first_action['actor']:
                    print(first_action['actor']['login'])
                    return first_action['actor']['login']
        
        return None

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None
