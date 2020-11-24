class Transaction:
    def __init__(self, contact, purpose, date, amount, transaction_type):
        self.contact = contact
        self.purpose = purpose
        self.date = date
        self.amount = amount
        self.type = transaction_type

    def to_csv(self):
        pass