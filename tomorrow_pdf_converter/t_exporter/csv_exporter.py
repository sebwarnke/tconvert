import csv


def write_csv(statement, file_path):
    with open(file_path, "w") as csv_file:

        print("filepath: " + file_path)

        fieldnames = ["amount", "bic", "iban", "contact", "purpose", "date", "type"]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for transaction in statement.transactions:
            writer.writerow(transaction.__dict__)

        csv_file.close()
