import argparse
import re
import transaction
from py_pdf_parser.loaders import load_file
from py_pdf_parser.components import PDFDocument

date_sep_regex = "^(MONTAG|DIENSTAG|MITTWOCH|DONNERSTAG|FREITAG|SAMSTAG|SONNTAG),\s(\d{1,2}\.\s(JANUAR|FEBRUAR|MÄRY|APRIL|MAI|JUNI|JULI|AUGUST|SEPTEMBER|OKTOBER|NOVEMBER|DEZEMBER)\s\d{4})$"
date_regex = "^\D*(\d{1,2})\.\s(JANUAR|FEBRUAR|MÄRY|APRIL|MAI|JUNI|JULI|AUGUST|SEPTEMBER|OKTOBER|NOVEMBER|DEZEMBER)\s(\d{4})$"


def month_name_to_number(monthname):
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
    return isodate


class TomorrowParser:
    document: PDFDocument
    date_section_unique_names = []
    transaction_section_unique_names = []

    def __init__(self, pdf_document):
        self.document = pdf_document

    def find_date_section_elements(self):
        return self.document.elements.filter_by_regex(date_sep_regex)

    def find_closing_element(self):
        element_list = self.document.elements.filter_by_text_equal("ZUSAMMENFASSUNG")
        if (element_list.__len__() > 1):
            exit(-1)
        else:
            return element_list.extract_single_element();

    def create_date_sections(self, date_section_elements, closing_element):
        # iterate length of ElementList
        for i in range(date_section_elements.__len__()):
            name = convert_to_iso_date(date_section_elements.__getitem__(i))

            # for the last element of ElementList
            if i == date_section_elements.__len__() - 1:
                unique_name = self.document.sectioning.create_section(name, date_section_elements.__getitem__(i),
                                                                      closing_element).unique_name
            # ... for all other elements
            else:
                unique_name = self.document.sectioning.create_section(name, date_section_elements.__getitem__(i),
                                                                      date_section_elements.__getitem__(i + 1),
                                                                      False).unique_name
            self.date_section_unique_names.append(unique_name)

    def process(self):
        closing_element = self.find_closing_element()
        date_section_elements = self.find_date_section_elements()
        self.create_date_sections(date_section_elements, closing_element)
        self.tag_transaction_section_elements_with_date()

    def tag_transaction_section_elements_with_date(self):
        for date_section_unique_name in self.date_section_unique_names:

            date_section = self.document.sectioning.get_section(date_section_unique_name)

            transaction_headers = date_section.elements.filter_by_font("QBKQTR+SimplonNorm-Medium-Identity-H,9.0")
            for i in range(transaction_headers.__len__()):
                if i < transaction_headers.__len__() - 1:
                    transaction_section_unique_name = self.document.sectioning.create_section(
                        date_section.name + "_" + transaction_headers.__getitem__(i).text(),
                        transaction_headers.__getitem__(i), transaction_headers.__getitem__(i + 1)).unique_name
                else:
                    transaction_section_unique_name = self.document.sectioning.create_section(
                        date_section.name + "_" + transaction_headers.__getitem__(i).text(),
                        transaction_headers.__getitem__(i),
                        date_section.elements.__getitem__(date_section.elements.__len__() - 1)).unique_name
                self.transaction_section_unique_names.append(transaction_section_unique_name)

        for unique_name in self.transaction_section_unique_names:
            section = self.document.sectioning.get_section(unique_name)
            print(section.name)
            for element in section.elements:
                print("  " + element.text())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()
    document = load_file(args.file_path)
    tomorrow_parser = TomorrowParser(document)
    tomorrow_parser.process()
