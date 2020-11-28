class Transaction:
    def __init__(self, date, amount, purpose, contact, iban_bic, transaction_type):
        self.date = date
        self.contact = contact
        self.purpose = purpose
        self.amount = amount
        self.type = transaction_type

        if iban_bic is not None:
            self.iban = iban_bic[0]
            self.bic = iban_bic[1]
        else:
            self.iban = None
            self.bic = None

    def __str__(self):
        return str(self.__dict__)

    def to_csv(self):
        pass