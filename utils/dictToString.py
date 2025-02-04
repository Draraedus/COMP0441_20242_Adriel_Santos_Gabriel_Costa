def dict_to_string(issue: dict) -> str:
    """
    Transforma uma única issue em formato de dicionário do python em uma string formatada.
    
    Args:
        dict: issue no formato dicionário a ser convertida em string.
    
    Returns:
        string: String formatada com os dados de título, corpo e comentários da issue.
    """
    issue_comment = ""
    try:
        for comment in issue['comments']:
            issue_comment += comment['body'] + "\n"
        
        string_from_dict = f"Título: {issue['issue']['title']}\nDescrição: {issue['issue']['body']} \nComentários: {issue_comment}"

        return string_from_dict
    except Exception as e:
        print(f"Erro dict_to_string: {e}")
        return None
