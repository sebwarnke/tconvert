class Transaction:
    def __init__(self, contact, purpose, date, amount):
        self.contact = contact
        self.purpose = purpose
        self.date = date
        self.amount = amount



    def to_csv(self):
        return ""