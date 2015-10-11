# models.py
import pytz
utc = pytz.utc
from project import db

Column = db.Column
TEXT = db.TEXT
DATETIME = db.DATETIME
DECIMAL = db.DECIMAL(9,6)
Integer = db.Integer


class TZDateTime(db.TypeDecorator):
    """
    Coerces a tz-aware datetime object into a naive utc datetime object to be
    stored in the database. If already naive, will keep it.

    On return of the data will restore it as an aware object by assuming it
    is UTC.

    Use this instead of the standard :class:`sqlalchemy.types.DateTime`.
    """

    impl = DATETIME

    def process_bind_param(self, value, dialect):
        if value.tzinfo is not None:
            value = value.astimezone(utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value.tzinfo is None:
            value = utc.localize(value)
        return value


class FXQuotes(db.Model):
    __tablename__ = 'fx_quotes'
    primary_key = Column(Integer, primary_key=True)
    provider = Column(TEXT, nullable=False)
    provider_href = Column(TEXT, nullable=False)
    quote_time = Column(DATETIME, nullable=False)
    source_currency = Column(TEXT, nullable=False)
    target_currency = Column(TEXT, nullable=False)
    fee = Column(DECIMAL, nullable=False)
    source_value = Column(DECIMAL, nullable=False)
    target_value = Column(DECIMAL, nullable=False)

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
