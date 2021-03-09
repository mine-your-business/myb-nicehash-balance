import json
import os

from .configuration import Configuration
from nicehash import NiceHashPrivateApi
from coindesk import CoindeskApi
from newrelic import NewRelicInsightsApi

def lambda_handler(event, context):
    """Lambda function reacting to EventBridge events

    Parameters
    ----------
    event: dict, required
        Event Bridge Scheduled Events Format

        Event doc: https://docs.aws.amazon.com/eventbridge/latest/userguide/event-types.html#schedule-event-type

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    """

    dry_run = os.environ.get('RUN_MODE') == 'test'
    print(f'Running in {"dry run" if dry_run else "production"} mode')

    config = Configuration()

    nicehash = NiceHashPrivateApi(
        config.nicehash.api_url, 
        config.nicehash.organization_id, 
        config.nicehash.wallet_api_key, 
        config.nicehash.wallet_api_secret
    )
    coindesk = CoindeskApi(
        config.coindesk.api_url,
        config.coindesk.currency,
        verbose=True
    )
    newrelic = NewRelicInsightsApi(
        config.newrelic.account_id,
        config.newrelic.insights.insert_api_key,
        config.newrelic.insights.query_api_url,
        config.newrelic.insights.insert_api_url,
        verbose=True
    )

    currency_price = coindesk.current_price(config.nicehash.cryptocurrency)
    print(f'Got current {config.nicehash.cryptocurrency} {config.coindesk.currency} '\
        f'price: {json.dumps(currency_price.__dict__, indent=2)}')

    btc_account = nicehash.get_accounts_for_currency(config.nicehash.cryptocurrency)
    if 'available' in btc_account:
        available_bal = float(btc_account['available'])
    else:
        print(f'Something changed in the API contract for {config.nicehash.cryptocurrency} '\
            '- couldn\'t find \'available\' balance')
        exit(1)

    print(f'Current available balance ({config.nicehash.cryptocurrency}): {available_bal}')


    event_type = 'MiningBalanceSnapshot'
    if dry_run:
        event_type = f'Test{event_type}'
    event = {
        'available_balance': available_bal,
        'balance_currency': config.nicehash.cryptocurrency,
        f'current_{config.nicehash.cryptocurrency.lower()}_{config.coindesk.currency.lower()}_price': currency_price.price,
        'price_currency': config.coindesk.currency,
        'btc_usd_price_updated_at': currency_price.updated_at,
        f'balance_value_{config.coindesk.currency}': available_bal * currency_price.price
    }

    insert_result = newrelic.insert_event(event_type, event)
    if insert_result:
        print(f'Successfully sent {event_type} event with data: {json.dumps(event, indent=2)}')

    # We got here successfully!
    return True
