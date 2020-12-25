from argparse import ArgumentParser
from py_pdf_parser.loaders import load_file
from tomorrow_pdf_converter.t_parser.tomorrow_parser import TomorrowParser
from tomorrow_pdf_converter.t_exporter.csv_exporter import write_csv


def main():
    parser = ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()
    document = load_file(args.file_path)

    print("Parsing PDF: " + args.file_path)

    if document is not None:
        tomorrow_parser = TomorrowParser(document)
        statement = tomorrow_parser.run()
        write_csv(statement, args.file_path.replace(".pdf", ".csv"))

    else:
        print("Document not found at path [" + args.filepath + "]")
        exit(-1)


if __name__ == "__main__":
    main()
