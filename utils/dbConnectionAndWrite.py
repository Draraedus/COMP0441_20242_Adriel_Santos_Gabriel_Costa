import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def insert_issues(issues):
    connection_db = psycopg2.connect(
        host=os.getenv("ISSUE_MINER_HOST"),
        database=os.getenv("ISSUE_MINER_DATABASE"),
        user=os.getenv("ISSUE_MINER_USUARIO"),
        password=os.getenv("ISSUE_MINER_SENHA"),
        port=os.getenv("ISSUE_MINER_PORT")
    )
    
    cursor = connection_db.cursor()
    
    for issue in issues:
        tema_relacionado = issue["tema_relacionado"]
        titulo = issue["titulo"]
        data_de_abertura = issue["data_de_abertura"]
        data_de_conclusao = issue["data_de_conclusao"]
        tempo_de_resolucao = issue["tempo_de_resolucao"]
        milestone = issue["milestone"]
        autor = issue["autor"]
        dev_responsavel = issue["dev_responsavel"]
        
        cursor.execute("""
            INSERT INTO issues.issue (
                tema_relacionado,
                titulo,
                data_de_abertura,
                data_de_conclusao,
                tempo_de_resolucao,
                milestone,
                autor,
                dev_responsavel
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            tema_relacionado,
            titulo,
            data_de_abertura,
            data_de_conclusao,
            tempo_de_resolucao,
            milestone,
            autor,
            dev_responsavel
        ))
    
    connection_db.commit()
    cursor.close()
    connection_db.close()