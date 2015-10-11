# views.py
from flask import (flash, redirect, render_template, request, session,
    url_for)

from project import app, db
from forms import QueryFXQuotes
from models import FXQuotes


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'error')


@app.route('/',  methods=['GET', 'POST'])
def quote_table():
    form = QueryFXQuotes(request.form)

    current_view = db.session.query(FXQuotes)
    if request.method == 'GET':
        return render_template('fx_quotes.html', form=form,
                               current_view=current_view)

    if request.method == 'POST':

        current_view = db.session.query(FXQuotes)

        if form.source_currency.data != 'All':
            current_view = current_view.filter_by(
                source_currency=form.source_currency.data)

        if form.target_currency.data != 'All':
            current_view = current_view.filter_by(
                target_currency=form.target_currency.data)

        if form.source_value.data != 'All':
            current_view = current_view.filter_by(
                source_value=form.source_value.data)

        return render_template('fx_quotes.html',
                               form=form,
                               current_view=current_view)

