import argparse
from py_pdf_parser.loaders import load_file
from src.parser.tomorrow_parser import TomorrowParser
from src.exporter.csv_exporter import write_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()
    document = load_file(args.file_path)

    if document is not None:
        tomorrow_parser = TomorrowParser(document)
        statement = tomorrow_parser.run()
        write_csv(statement, args.file_path.replace(".pdf", ".csv"))

    else:
        print("Document not found at path [" + args.filepath + "]")
        exit(-1)
