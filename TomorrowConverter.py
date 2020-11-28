import argparse
from py_pdf_parser.loaders import load_file
from TomorrowParser import TomorrowParser

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()
    document = load_file(args.file_path)

    if document is not None:
        tomorrow_parser = TomorrowParser(document)
        tomorrow_parser.run()
    else:
        print("Document not found at path [" + args.filepath + "]")
        exit(-1)
