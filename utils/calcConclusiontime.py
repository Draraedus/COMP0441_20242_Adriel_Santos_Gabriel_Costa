from datetime import datetime

def calculate_duration(start_date, end_date) -> str:
    """
    Função que calcula a duração de uma issue a partir das datas de início e fim.
    
    Args:
        start_date (str): Data de início da issue no formato ISO 8601.
        end_date (str): Data de fim da issue no formato ISO 8601.
    
    Returns:
        float: Duração da issue em dias.
    """

    try:
        format_string = "%Y-%m-%dT%H:%M:%SZ"
        start_datetime = datetime.strptime(start_date, format_string)
        end_datetime = datetime.strptime(end_date, format_string)
        duration = end_datetime - start_datetime
        duration_in_days = duration.total_seconds() / (24 * 60 * 60)
    except Exception as e:
        print(f"Erro calculate_duration: {e}")
        return None

    return str(duration_in_days.__format__(".1f"))
