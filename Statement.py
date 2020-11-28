class Statement:
    transactions = []

    def append_transaction(self, transaction):
        self.transactions.append(transaction)

    def print(self):
        for transaction in self.transactions:
            print(str(transaction))