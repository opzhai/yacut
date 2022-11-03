from flask import render_template, redirect, flash, abort, request
from . import app, db
from .forms import URL_mapForm
from .models import URL_map
from string import ascii_letters, digits
import random


def get_unique_short_id():
    LETTER = (set(ascii_letters) | set(digits))
    link = "".join(random.sample(LETTER, 6))
    return link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URL_mapForm()
    host_url = request.host_url
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        if custom_id == "" or custom_id is None:
            custom_id = get_unique_short_id()
        if URL_map.query.filter_by(short=custom_id).first() is not None:
            flash(f'Имя {form.custom_id.data} уже занято!')
            return render_template('index.html', form=form)
        if URL_map.query.filter_by(original=original).first() is not None:
            flash('Для данной сслыки уже существует короткая версия!')
            return render_template('index.html', form=form)
        if URL_map.query.filter_by(short=custom_id).first() is not None:
            flash('Данная ссылка уже используется!')
            return render_template('index.html', form=form)
        url = URL_map(
            original=original,
            short=custom_id,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form, host_url=host_url, short_link=url.short)
    return render_template('index.html', form=form)


@app.route('/<string:short_url>', methods=['GET'])
def redirect_short_view(short_url):
    url = URL_map.query.filter_by(short=short_url).first()
    if url is None:
        abort(404)
    return redirect(url.original, 302)
