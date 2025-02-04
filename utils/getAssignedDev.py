import requests

def get_first_timeline_author(issue: dict) -> str:
    """
    Função que busca o autor da primeira ação realizada na timeline em uma issue.
    
    Args:
        issue_link (str): URL da issue no GitHub.
    
    Returns:
        str: Login do autor da primeira ação na timeline.
    """
    
    if issue['timeline_url'] != "":
        timeline_link = issue['timeline_url']
        
        timeline_response = requests.get(timeline_link)
        
        if timeline_response.status_code == 200:
            timeline = timeline_response.json()
            
            first_action = timeline[0]
            first_action_author = first_action['actor']['login']

            return first_action_author
    
    return None