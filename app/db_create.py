# db_create.py

from datetime import datetime
from views import db
from models import FXQuotes

if __name__ == '__main__':
    # create the database and the db table
    db.create_all()

    # add one row of sample data - this is actual data
    quote_time = datetime(year=2015, month=9, day=30,
                          hour=21, minute=36, second=50)

    row_obj = FXQuotes(provider='TransferWise',
                       provider_href='https:/www.transferwise.com',
                       details='Transfer from UK to US bank account',
                       quote_time=quote_time,
                       source_currency='GBP',
                       target_currency='USD',
                       fee=1.0,
                       source_value=100.0,
                       target_value=149.76)

    db.session.add(row_obj)

    # commit the changes
    db.session.commit()

