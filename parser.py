import argparse
import transaction
from py_pdf_parser.loaders import load_file
from py_pdf_parser.components import PDFDocument


class TomorrowDocument:
    document: PDFDocument

    DATE_SEP_REGEX = "^(MONTAG|DIENSTAG|MITTWOCH|DONNERSTAG|FREITAG|SAMSTAG|SONNTAG),\s(\d{1,2}\.\s(JANUAR|FEBRUAR|MÄRY|APRIL|MAI|JUNI|JULI|AUGUST|SEPTEMBER|OKTOBER|NOVEMBER|DEZEMBER)\s\d{4})$"

    def __init__(self, pdf_document):
        self.document = pdf_document

    def find_date_sections(self):
        elements = self.document.elements.filter_by_regex(self.DATE_SEP_REGEX)
        for element in elements:
            print(element.text())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()
    document = load_file(args.file_path)
    tomorrow_document = TomorrowDocument(document)
    tomorrow_document.find_date_sections()