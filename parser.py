import argparse
import re
import transaction
from py_pdf_parser.loaders import load_file
from py_pdf_parser.components import PDFDocument

date_sep_regex = "^(MONTAG|DIENSTAG|MITTWOCH|DONNERSTAG|FREITAG|SAMSTAG|SONNTAG),\s(\d{1,2}\.\s(JANUAR|FEBRUAR|MÄRY|APRIL|MAI|JUNI|JULI|AUGUST|SEPTEMBER|OKTOBER|NOVEMBER|DEZEMBER)\s\d{4})$"
date_regex = "^\D*(\d{1,2})\.\s(JANUAR|FEBRUAR|MÄRY|APRIL|MAI|JUNI|JULI|AUGUST|SEPTEMBER|OKTOBER|NOVEMBER|DEZEMBER)\s(\d{4})$"

def month_name_to_number (monthname):
    if monthname == "JANUAR":
        return "1"
    if monthname == "FEBRUAR":
        return "2"
    if monthname == "MÄRZ":
        return "3"
    if monthname == "APRIL":
        return "4"
    if monthname == "MAI":
        return "5"
    if monthname == "JUNI":
        return "6"
    if monthname == "JULI":
        return "7"
    if monthname == "AUGUST":
        return "8"
    if monthname == "SEPTEMBER":
        return "9"
    if monthname == "OKTOBER":
        return "10"
    if monthname == "NOVEMBER":
        return "11"
    if monthname == "DEZEMBER":
        return "12"


def convert_to_iso_date(date_section_title):
    match = re.search(date_regex, date_section_title.text())
    if match is not None:
        isodate = match.group(3) + '-' + month_name_to_number(match.group(2)) + '-'
        if int(match.group(1)) < 10:
            isodate = isodate + "0" + match.group(1)
        else:
            isodate = isodate + match.group(1)

class TomorrowDocument:
    document: PDFDocument

    def __init__(self, pdf_document):
        self.document = pdf_document

    def find_date_section_elements(self):
        return self.document.elements.filter_by_regex(date_sep_regex)

    def create_sections(self, date_section_elements):
        # iterate length of ElementList
        for i in range(date_section_elements.__len__()-1):
            name = convert_to_iso_date(date_section_elements.__getitem__(i))
            # for the last element of ElementList
            if i == date_section_elements.__len__() - 1:
                section = self.document.sectioning.create_section(name, date_section_elements.__getitem__(i),
                                                             date_section_elements.__getitem__(i + 1))
            # ... for all other elements
            # else:
            #     self.document.sectioning.create_section(date_section_elements.__getitem__(i),)

    def process(self):
        date_section_elements = self.find_date_section_elements()
        self.create_sections(date_section_elements)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()
    document = load_file(args.file_path)
    tomorrow_document = TomorrowDocument(document)
    tomorrow_document.process()