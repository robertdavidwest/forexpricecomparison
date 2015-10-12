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


def ozforex(FromCurrency, ToCurrency, FromAmount):

    url = 'http://www.ozforex.com.au/currency-converter-martini'
    data = {
        'FromAmount': FromAmount,
        'FromCurrency': FromCurrency,
        'ToCurrency': ToCurrency
    }
    response = requests.post(url, data=data)
    content = response.content.replace('null', '""')
    results = ast.literal_eval(content)
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
    providers = []
    providers_href = []
    sourceValues = []
    details = []

    def add_row(targetValue, sourceValue, quotetime, fee, provider,
                provider_href, detail):
        '''

        '''
        targetValues.append(targetValue)
        sourceValues.append(sourceValue)
        quotetimes.append(quotetime)
        fees.append(fee)
        providers.append(provider)
        providers_href.append(provider_href)
        details.append(detail)

    sourceValuesForLoop = [100, 500, 1000, 5000, 10000, 50000, 100000]
    for sourceValue in sourceValuesForLoop:

        ### Transferwise Scrape ###
        results_transferwise = scrape_transferwise(
            sourceValue=sourceValue,
            sourceCurrencyCode=sourceCurrencyCode,
            targetCurrencyCode=targetCurrencyCode
        )
        targetValue = float(results_transferwise['targetValue'].replace(',', ''))
        fee = float(results_transferwise['fee'].replace(',', ''))

        add_row(targetValue=targetValue,
                sourceValue=sourceValue,
                quotetime=results_transferwise['date'],
                fee=fee,
                provider='TransferWise',
                provider_href='transferwise.com',
                detail='Transfer from US to UK bank account'
                )

        ### OzForex Scrape ###
        results_oz = ozforex(FromCurrency=sourceCurrencyCode,
                             ToCurrency=targetCurrencyCode,
                             FromAmount=sourceValue)
        # OzForex has a flat fee on transactions under 10,000 AUD, I convert this
        # to USD and apply. Really this is probably only available from Aus
        # but this should give a good initial view of the price available at
        # USForex does not have a quote without a login
        r = ozforex(FromCurrency='AUD', ToCurrency='USD', FromAmount=10000)
        use_min_for_fee = r['ToAmount']
        aud_usd = r['FromRate']
        if sourceValue < use_min_for_fee:
            fee = 15*aud_usd
        else:
            fee = 0

        add_row(targetValue=results_oz['ToAmount'],
                sourceValue=sourceValue,
                quotetime=results_oz['date'],
                fee=fee,
                provider='OzForex',
                provider_href='http://www.ozforex.com.au/',
                detail='*No fees for transfers over AUD$10,000. $15 flat fee '
                       'per recipient for transfers under AUD$10,000 '
                       '**Rates subject to change and for individuals only'
                )

        ### Travelex Scrape ###
        results_travelex = scrape_travelex(targetCurrencyCode='GBP', site='us')

        rate = float(results_travelex['rate'])
        targetValue = sourceValue * rate

        if sourceValue < 250:
            fee =  sqlalchemy.sql.null()
            targetValue = sqlalchemy.sql.null()
        elif (250 <= sourceValue) & (sourceValue < 1000):
            fee = 9.99
        else:
            fee = 0

        add_row(targetValue=targetValue,
                sourceValue=sourceValue,
                quotetime=results_travelex['date'],
                fee=fee,
                provider='Travelex - Cash',
                provider_href='www.travelex.com/rates',
                detail='Pay USD online, GBP Cash delivered, free Next Day Delivery '
                       'on orders above $1000, no orders below $250'
                )

    results_df = pd.DataFrame({'fee': fees,
                               'source_value': sourceValues,
                               'target_value': targetValues,
                               'source_currency': sourceCurrencyCode,
                               'target_currency': targetCurrencyCode,
                               'quote_time': quotetimes,
                               'provider': providers,
                               'provider_href': providers_href,
                               'details': details,
                               })
    import ipdb; ipdb.set_trace()
    results_df.to_sql(name='fx_quotes', con=db.engine, if_exists='append', index=False)