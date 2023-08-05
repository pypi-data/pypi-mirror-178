class CustomerBankAccount(object):
    """A thin wrapper around a customer_bank_account, providing easy access to its
    attributes.

    Example:
      customer_bank_account = client.customer_bank_accounts.get()
      customer_bank_account.mandate_reference
    """

    def __init__(self, attributes, api_response):
        self.attributes = attributes
        self.api_response = api_response

    @property
    def id(self):
        return self.attributes.get('id')

    @property
    def customer_reference(self):
        return self.attributes.get('customer_reference')

    @property
    def mandate_reference(self):
        return self.attributes.get('mandate_reference')

    @property
    def hidden_iban(self):
        return self.attributes.get('hidden_iban')

    @property
    def created_at(self):
        return self.attributes.get('created_at')

    @property
    def sepa_type(self):
        return self.attributes.get('sepa_type')

    @property
    def mandate_status(self):
        return self.attributes.get('mandate_status')

    @property
    def metadata(self):
        return self.attributes.get('metadata')
