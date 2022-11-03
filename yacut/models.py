from datetime import datetime
from flask import request
from urllib.parse import urljoin
from . import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, unique=True, nullable=False)
    short = db.Column(db.String, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        host_url = request.host_url
        return dict(
            url=self.original,
            short_link=urljoin(host_url, self.short)
        )

    def from_dict(self, data):
        setattr(self, 'short', data['custom_id'])
        setattr(self, 'original', data['url'].strip())
