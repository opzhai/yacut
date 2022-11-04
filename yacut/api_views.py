from flask import jsonify, request
from . import app, db
from .models import URL_map
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage
import re
from http import HTTPStatus


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URL_map.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    data = url.to_dict()
    return jsonify({'url': data['url']}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    link_template = re.compile('^[A-Za-z0-9]{1,16}$')
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] is None or data['custom_id'] == '':
        data['custom_id'] = get_unique_short_id()
    elif len(data['custom_id']) > 16 or not link_template.match(data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    elif URL_map.query.filter_by(short=data['custom_id']).first() is not None:
        short = data['custom_id']
        raise InvalidAPIUsage(f'Имя "{short}" уже занято.')
    url = URL_map()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED
