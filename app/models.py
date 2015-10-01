# models.py

from views import db

class FXQuotes(db.Model):
    __tablename__ = 'fx_quotes'
    primary_key = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String, nullable=False)
    provider_href = db.Column(db.String, nullable=False)
    quote_time = db.Column(db.DATETIME, nullable=False)
    source_currency = db.Column(db.String, nullable=False)
    target_currency = db.Column(db.String, nullable=False)
    fee = db.Column(db.DECIMAL, nullable=False)
    source_value = db.Column(db.DECIMAL, nullable=False)
    target_value = db.Column(db.DECIMAL, nullable=False)

    def __init__(self, provider, provider_href, quote_time, source_currency,
                 target_currency, fee, source_value, target_value):

        self.provider = provider
        self.provider_href = provider_href
        self.quote_time = quote_time
        self.source_currency = source_currency
        self.target_currency = target_currency
        self.fee = fee
        self.source_value = source_value
        self.target_value = target_value

    def __repr__(self):
        return '<fx_quotes %r>' %(self.fx_quotes)
