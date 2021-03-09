import os

class Configuration:

    def __init__(self):
        self.nicehash = NiceHash()
        self.newrelic = NewRelic()
        self.coindesk = Coindesk()

class NiceHash:

    def __init__(self):
        self.organization_id = os.environ.get('NICE_HASH_ORG_ID')
        self.wallet_api_key = os.environ.get('NICE_HASH_WALLET_API_KEY')
        self.wallet_api_secret = os.environ.get('NICE_HASH_WALLET_API_SECRET')
        self.api_url = os.environ.get('NICE_HASH_API_URL')
        self.cryptocurrency = os.environ.get('NICE_HASH_CRYPTOCURRENCY')

class NewRelicInsights:

    def __init__(self):
        self.insert_api_key = os.environ.get('NEWRELIC_INSIGHTS_INSERT_API_KEY')
        self.query_api_url = os.environ.get('NEWRELIC_INSIGHTS_QUERY_API_URL')
        self.insert_api_url = os.environ.get('NEWRELIC_INSIGHTS_INSERT_API_URL')

class NewRelic:

    def __init__(self):
        self.account_id = os.environ.get('NEWRELIC_ACCOUNT_ID')
        self.insights = NewRelicInsights()

class Coindesk:

    def __init__(self):
        self.api_url = os.environ.get('COINDESK_API_URL')
        self.currency = os.environ.get('COINDESK_CURRENCY')
