import re

from py_pdf_parser.components import PDFDocument
from py_pdf_parser.components import PDFElement
from src.parser.transaction import Transaction
from src.parser.statement import Statement

closing_element_text = "ZUSAMMENFASSUNG"

# This regex matches the headline of each per day transaction section in a Tomorrow Document
date_sep_regex = "^(MONTAG|DIENSTAG|MITTWOCH|DONNERSTAG|FREITAG|SAMSTAG|SONNTAG),\s(\d{1,2}\.\s(JANUAR|FEBRUAR|MÄRZ|APRIL|MAI|JUNI|JULI|AUGUST|SEPTEMBER|OKTOBER|NOVEMBER|DEZEMBER)\s\d{4})$"

# This regex matches the date string of the above headline.
date_regex = "^\D*(\d{1,2})\.\s(JANUAR|FEBRUAR|MÄRZ|APRIL|MAI|JUNI|JULI|AUGUST|SEPTEMBER|OKTOBER|NOVEMBER|DEZEMBER)\s(\d{4})$"


def extract_purpose(section):
    if section.elements.__len__() >= 5:
        purpose = section.elements.__getitem__(section.elements.__len__() - 1).text()
    else:
        purpose = None
    return purpose


def extract_transaction_type(section):
    return section.elements.filter_by_regex("Überweisung|Kartenzahlung").extract_single_element().text()


def extract_contact(section):
    return section.elements.__getitem__(0).text()


def extract_amount(section):
    amount = section.elements.filter_by_regex("^[+|-](((?:[1-9]\d{0,2}(,\d{3})*)|0)?\.\d{1,2})\s€$") \
        .extract_single_element().text()
    return amount.strip("+€ ").replace(",", "")


def extract_iban_bic(section):
    iban_bic = section.elements.filter_by_text_contains("IBAN").extract_single_element().text()
    match_iban = re.search("[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})?", iban_bic)
    match_bic = re.search("BIC:\s(\w+)", iban_bic)
    if match_iban is not None and match_bic is not None:
        return match_iban.group(0), match_bic.group(0)
    else:
        return None


def extract_date(section):
    return section.name[0:10]


class TomorrowParser:
    document: PDFDocument
    closing_element: PDFElement
    date_section_unique_names = []
    transaction_section_unique_names = []
    statement: Statement

    def __init__(self, pdf_document):
        self.document = pdf_document
        self.statement = Statement()

    def run(self):
        self.ignore_footers()
        self.find_closing_element()
        self.create_date_sections()
        self.create_transaction_sections()
        self.parse_transaction_sections()
        return self.statement

    def find_closing_element(self):
        element_list = self.document.elements.filter_by_text_equal(closing_element_text)
        if element_list.__len__() > 1:
            print(
                "Found more than one element with text ['" + closing_element_text + "']. Expected only one to be the closing element.")
            exit(-1)
        else:
            self.closing_element =  element_list.extract_single_element();

    # When this method returns we identified and created all sections referring to a date a transaction took place.
    # Each section was assigned a unique name which we stored.
    def create_date_sections(self):
        date_section_elements = self.document.elements.filter_by_regex(date_sep_regex)
        # iterate length of ElementList
        for i in range(date_section_elements.__len__()):
            name = convert_to_iso_date(date_section_elements.__getitem__(i))

            # for the last element of ElementList
            if i == date_section_elements.__len__() - 1:
                unique_name = self.document.sectioning.create_section(name, date_section_elements.__getitem__(i),
                                                                      self.closing_element, False).unique_name
            # ... for all other elements
            else:
                unique_name = self.document.sectioning.create_section(name, date_section_elements.__getitem__(i),
                                                                      date_section_elements.__getitem__(i + 1),
                                                                      False).unique_name
            self.date_section_unique_names.append(unique_name)

    # When this method returns we identified and created all sections referring to an individual transaction.
    # Each section was assigned a unique name which we stored.
    def create_transaction_sections(self):
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

        # for unique_name in self.transaction_section_unique_names:
        #     section = self.document.sectioning.get_section(unique_name)
        #     print(section.name)
        #     for element in section.elements:
        #         print("  " + element.text())

    # This method iterates the transaction sections and parses each into a transaction object.
    def parse_transaction_sections(self):
        for unique_name in self.transaction_section_unique_names:
            section = self.document.sectioning.get_section(unique_name)
            amount = extract_amount(section)
            contact = extract_contact(section)
            transaction_type = extract_transaction_type(section)
            iban_bic = extract_iban_bic(section)
            purpose = extract_purpose(section)
            date = extract_date(section)

            transaction = Transaction(date, amount, purpose, contact, iban_bic, transaction_type)
            self.statement.append_transaction(transaction)

    def ignore_footers(self):
        self.document.elements.filter_by_text_contains("Erstellt am").ignore_elements()


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
