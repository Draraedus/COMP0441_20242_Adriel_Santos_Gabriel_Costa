import csv
import datetime

def csv_create_and_write(data):
    actual_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"result_{actual_date}.csv"

    with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
        field_names = list(data[0].keys())
        escritor_csv = csv.DictWriter(arquivo_csv, dialect='excel', fieldnames=field_names, delimiter=';')
        escritor_csv.writeheader()
        escritor_csv.writerows(data)