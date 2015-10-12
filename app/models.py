# models.py
from views import db

Column = db.Column
TEXT = db.TEXT
DATETIME = db.DATETIME
NUMERIC = db.Numeric(20, 3)
Integer = db.Integer

class FXQuotes(db.Model):
    __tablename__ = 'fx_quotes'
    primary_key = Column(Integer, primary_key=True)
    provider = Column(TEXT, nullable=False)
    provider_href = Column(TEXT, nullable=False)
    details = Column(TEXT, nullable=False)
    quote_time = Column(DATETIME, nullable=False)
    source_currency = Column(TEXT, nullable=False)
    target_currency = Column(TEXT, nullable=False)
    fee = Column(NUMERIC, nullable=False)
    source_value = Column(NUMERIC, nullable=False)
    target_value = Column(NUMERIC, nullable=False)

    def __init__(self, provider, provider_href, details, quote_time,
                 source_currency, target_currency, fee, source_value,
                 target_value):

        self.provider = provider
        self.provider_href = provider_href
        self.details = details
        self.quote_time = quote_time
        self.source_currency = source_currency
        self.target_currency = target_currency
        self.fee = fee
        self.source_value = source_value
        self.target_value = target_value

    def __repr__(self):
         return '<fx_quotes %r>' %(self.fx_quotes)
