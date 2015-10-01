import requests
import ast
import pandas as pd

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
    results['date'] = pd.to_datetime(response.headers['date'], utc=True)
    import ipdb; ipdb.set_trace()
    return results



#sourceCurrencyCode = 'GBP'
#targetCurrencyCode = 'USD'


availableSourceCurrencies = ['EUR','GBP', 'USD', 'PLN', 'CHF', 'NOK', 
                            'SEK', 'DKK', 'AUD', 'HUF', 'GEL', 'RON',
                            'CZK', 'BGN'] 

availableTargeteCurrencies = ['EUR','GBP', 'USD', 'PLN', 'CHF', 'NOK', 
                              'SEK', 'DKK', 'AUD', 'CAD', 'HUF', 'GEL', 
                              'HKD', 'INR', 'IDR', 'MYR', 'MXN', 'RON',
                              'TRY', 'NZD', 'PHP', 'SGD', 'THB', 'CZK',
                              'BGN', 'BRL', 'CLP', 'COP', 'NGN', 'PKR',
                              'MAD', 'AED', 'UAH']

sourceCurrencyCode = 'GBP'
targetCurrencyCode = 'USD'
sourceValues = [100] #, 500, 1000, 5000, 10000, 50000, 100000]
targetValues = []
quotetimes = []
fees = []
provider = 'transferwise.com'

for sourceValue in sourceValues:

    results = scrape_transferwise(
        sourceValue=sourceValue,
        sourceCurrencyCode=sourceCurrencyCode, 
        targetCurrencyCode=targetCurrencyCode
    )
    # str to float
    targetValue = float(results['targetValue'].replace(',', ''))
    fee = float(results['fee'].replace(',', ''))

    targetValues.append(targetValue)
    fees.append(fee)
    quotetimes.append(results['date'])

results_df = pd.DataFrame({'fee': fees,
                           'sourceValue': sourceValues,
                           'targetValue': targetValues,
                           'sourceCurrencyCode': sourceCurrencyCode,
                           'targetCurrencyCode': targetCurrencyCode,
                           'quotetime': quotetimes,
                           'provider': provider})
print results_df
