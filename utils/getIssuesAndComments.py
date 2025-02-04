import requests

def get_issues(repo: str, state: str, limit: int, token: str = None) -> list:
    """
    Busca as issues de um repositório no GitHub, lidando com paginação para capturar grandes ou pequenos números de issues a serem capturadas.
    
    Args:
        repo (str): Nome do repositório no formato 'owner/repo'.
        state (str): Estado das issues a serem buscadas ('open', 'closed' ou 'all').
        limit (int): Limite de issues a serem buscadas.
        token (str): Token de autenticação do GitHub (opcional).
    
    Returns:
        list: Lista de issues encontradas.
    """

    url = f"https://api.github.com/search/issues?q="
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    issues = []
    page = 1
    try :
        while len(issues) < limit:
            urlWithParams = f"{url}repo:{repo}+state:{state}&per_page={min(100, limit - len(issues))}&page={page}"
            response = requests.get(urlWithParams, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Erro ao buscar issues: {response.status_code} - {response.text}")
            
            batch = response.json()
            if not batch.get("items"):
                break
            
            issues.extend(batch["items"])
            page += 1
    except Exception as e:
        print(f"Erro get_issues: {e}")
        return []
    
    return issues[:limit]

def get_comments(issue_url: str, token: str = None) -> list:
    """
    Busca todos os comentários de uma issue específica.
    
    Args:
        issue_url (str): URL da issue no GitHub.
        token (str): Token de autenticação do GitHub (opcional).
    
    Returns:
        list: Lista de comentários da issue.
    """

    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if token:
        headers["Authorization"] = f"token {token}"
    
    response = requests.get(issue_url, headers=headers)
    
    if response.status_code != 200:
        return []
    
    return response.json()

def merge_issues_with_comments(repo: str, state: str, limit: int, token: str = None) -> list:
    """
    Obtém issues e seus comentários formatados em um array de objetos, além disso utiliza outras funções para buscar as issues no github.
    
    Args:
        repo (str): Nome do repositório no formato 'owner/repo'.
        state (str): Estado das issues a serem buscadas ('open', 'closed' ou 'all').
        limit (int): Limite de issues a serem buscadas.
        token (str): Token de autenticação do GitHub (opcional).
    
    Returns:
        list: Lista de objetos contendo as issues e seus comentários.
    """
    issues = get_issues(repo, state, limit, token)
    issues_list = []
    
    try:
        for issue in issues:
            if "pull_request" in issue:
                continue  # Ignorar pull requests
            
            comments = get_comments(issue["comments_url"], token)
            issues_list.append({
                "issue": issue,
                "comments": comments
            })
    except Exception as e:
        print(f"Erro merge_issues_with_comments: {e}")
    
    return issues_list
