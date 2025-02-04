import time

from utils.getIssuesAndComments import merge_issues_with_comments
from utils.issueClassification import classify_issue
from utils.calcConclusiontime import calculate_duration
from utils.getAssignedDev import get_first_timeline_author
from utils.csvCreateAndWrite import csv_create_and_write
from utils.dbConnectionAndWrite import insert_issues

def main():
    """Interface interativa para capturar input do usuário e buscar issues."""
    repo = input("Digite o repositório (exemplo: owner/repo): ")
    state = input("Digite o estado das issues (open, closed, all): ")
    limit = int(input("Digite a quantidade de issues a buscar: "))
    token = input("Digite seu token de autenticação do GitHub (ou pressione Enter para continuar sem): ").strip()
    token = token if token else None

    issues_filtered = []
    
    try:
        issues = merge_issues_with_comments(repo, state, limit, token)
        print(f"{len(issues)} issues encontradas.")
        
        for index, issue in enumerate(issues):
            issue_filtered = {}
            issue_filtered["tema_relacionado"] = classify_issue(issue)
            issue_filtered["titulo"] = issue['issue']['title']
            issue_filtered["data_de_abertura"] = issue['issue']['created_at']
            issue_filtered["data_de_conclusao"] = issue['issue']['closed_at']
            issue_filtered["tempo_de_resolucao"] = calculate_duration(issue_filtered["data_de_abertura"], issue_filtered["data_de_conclusao"])
            issue_filtered["milestone"] = issue['issue']["milestone"]["title"] if issue['issue']["milestone"] else None
            issue_filtered["autor"] = issue['issue']['user']['login']
            issue_filtered["dev_responsavel"] = get_first_timeline_author(issue['issue'])

            issues_filtered.append(issue_filtered)
            time.sleep(5)
        
        print("Issues filtradas com sucesso.")

        csv_create_and_write(issues_filtered)

        print("CSV criado e preenchido com sucesso.")

        insert_issues(issues_filtered)

        print("Dados inseridos no banco de dados com sucesso.")

        print("Operação finalizada com sucesso.\n Fim do Script.\n Sucesso!!")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
