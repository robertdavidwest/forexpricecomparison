import requests
import ast
import pandas as pd
import numpy as np
from views import db
import sqlalchemy

def scrape_transferwise(sourceValue, sourceCurrencyCode, targetCurrencyCode):

    currencyCodeToId = {'AED': 70, 'AUD': 9, 'BGN': 41, 'BRL': 42,
                    'CAD': 10, 'CHF': 5, 'CLP': 43, 'COP': 44,
                    'CZK': 40, 'DKK': 8, 'EUR': 1, 'GBP': 2,
                    'GEL': 15, 'HKD': 24, 'HUF': 14, 'IDR': 27,
                    'INR': 26, 'MAD': 65, 'MXN': 29, 'MYR': 28,
                    'NGN': 54, 'NOK': 6, 'NZD': 32, 'PHP': 33,
                    'PKR': 55, 'PLN': 4, 'RON': 30, 'SEK': 7,
                    'SGD': 35, 'THB': 38,'TRY': 31,'UAH': 82,
                    'USD': 3}

    sourceCurrencyId = currencyCodeToId[sourceCurrencyCode]
    targetCurrencyId = currencyCodeToId[targetCurrencyCode]

    url = 'https://transferwise.com/request/initiatePageRate?calculatorView=1&lang=us&invertSavings='
    data = {'fixType': 'SOURCE',
            'sourceValue': sourceValue,
            'sourceCurrencyId': sourceCurrencyId,
            'targetCurrencyId': targetCurrencyId
    }
    response = requests.post(url=url, data=data)
    results = ast.literal_eval(response.content)
    results['date'] = pd.to_datetime(response.headers['date'])

    return results


def scrape_travelex(targetCurrencyCode, site):
    '''Convert USD dollar into other currencies, specified by
    targetCurrencyCode in the amount sourceValue'''

    # sites - 'au', 'gb' or 'us'

    url = 'https://api.travelex.net/salt/rates/' \
          'current?key=Travelex&site=/{}&productCodes={}'.format(site,
                                                                 targetCurrencyCode)

    response = requests.get(url)
    content = response.content.replace('false', 'False')
    content = ast.literal_eval(content)

    results = {}
    results['date'] = pd.to_datetime(response.headers['date'])
    results['rate'] = content['rates'][targetCurrencyCode]
    return results


if __name__ == '__main__':
    scrape_travelex(targetCurrencyCode='GBP', site='us')

    # Transferwise available currencies
    availableSourceCurrencies = ['EUR','GBP', 'USD', 'PLN', 'CHF', 'NOK',
                                'SEK', 'DKK', 'AUD', 'HUF', 'GEL', 'RON',
                                'CZK', 'BGN']

    availableTargeteCurrencies = ['EUR','GBP', 'USD', 'PLN', 'CHF', 'NOK',
                                  'SEK', 'DKK', 'AUD', 'CAD', 'HUF', 'GEL',
                                  'HKD', 'INR', 'IDR', 'MYR', 'MXN', 'RON',
                                  'TRY', 'NZD', 'PHP', 'SGD', 'THB', 'CZK',
                                  'BGN', 'BRL', 'CLP', 'COP', 'NGN', 'PKR',
                                  'MAD', 'AED', 'UAH']

    sourceCurrencyCode = 'USD'
    targetCurrencyCode = 'GBP'

    targetValues = []
    quotetimes = []
    fees = []
    provider = []
    provider_href = []
    sourceValues = []
    details = []

    sourceValuesForLoop = [100, 500, 1000, 5000, 10000, 50000, 100000]
    for sourceValue in sourceValuesForLoop:

        # Transferwise Scrape
        results_transferwise = scrape_transferwise(
            sourceValue=sourceValue,
            sourceCurrencyCode=sourceCurrencyCode,
            targetCurrencyCode=targetCurrencyCode
        )

        # str to float
        targetValue = float(results_transferwise['targetValue'].replace(',', ''))
        fee = float(results_transferwise['fee'].replace(',', ''))

        targetValues.append(targetValue)
        sourceValues.append(sourceValue)
        fees.append(fee)
        quotetimes.append(results_transferwise['date'])
        provider.append('TransferWise')
        provider_href.append('transferwise.com')
        details.append('Transfer from US to UK bank account')

        # Travelex Scrape
        results_travelex = scrape_travelex(targetCurrencyCode='GBP', site='us')

        sourceValues.append(sourceValue)
        quotetimes.append(results_travelex['date'])
        provider.append('Travelex - Cash')
        provider_href.append('www.travelex.com/rates')
        details.append('Pay USD online, GBP Cash delivered, free Next Day Delivery on order above $1000, no orders below $250')

        rate = float(results_travelex['rate'])
        targetValue = sourceValue * rate

        if sourceValue < 250:
            fees.append(sqlalchemy.sql.null())
            targetValues.append(sqlalchemy.sql.null())
            details.append('Rate no available with source value below $250')
        elif (250 <= sourceValue) & (sourceValue < 1000):
            fees.append(9.99)
            targetValues.append(targetValue)
            details.append('Pay USD online, GBP Cash delivered, free Next Day Delivery on orders above $1000, no orders below $250')
        else:
            fees.append(0)
            targetValues.append(targetValue)
            details.append('Pay USD online, GBP Cash delivered, free Next Day Delivery on orders above $1000, no orders below $250')

    results_df = pd.DataFrame({'fee': fees,
                               'source_value': sourceValues,
                               'target_value': targetValues,
                               'source_currency': sourceCurrencyCode,
                               'target_currency': targetCurrencyCode,
                               'quote_time': quotetimes,
                               'provider': provider,
                               'provider_href': provider_href,
                               'details': details,
                               })

    results_df.to_sql(name='fx_quotes', con=db.engine, if_exists='append', index=False)