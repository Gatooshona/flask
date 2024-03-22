import flask
from flask import request, views, jsonify
from models import Session, Notice
from sqlalchemy.exc import IntegrityError
from app.errors import HttpError
from schema import CreateNotice, UpdateNotice
from tools import validate
from flask_bcrypt import Bcrypt


app = flask.Flask('app')
bcrypt = Bcrypt(app)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({'error': error.description})
    response.status_code = error.status_code
    return response


def get_notice(notice_id: int):
    notice = request.session.get(Notice, notice_id)
    if notice is None:
        raise HttpError(status_code=404, description='not found')
    return notice


def add_notice(notice: Notice):
    try:
        request.session.add(notice)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(status_code=409, description='notice already exists')


class NoticeView(views.MethodView):

    @property
    def session(self) -> Session:
        return request.session

    def get(self, notice_id: int):
        notice = get_notice(notice_id)
        return jsonify(notice.dict)

    def post(self):
        notice_data = validate(CreateNotice, request.json)
        notice = Notice(**notice_data)
        add_notice(notice)
        return jsonify({'id': 'notice.id'})

    def patch(self, notice_id: int):
        notice = get_notice(notice_id)
        notice_data = validate(UpdateNotice, request.json)
        for key, value in notice_data.items():
            setattr(notice, key, value)
            add_notice(notice)
        return jsonify({'id': 'notice.id'})



    def delete(self, notice_id: int):
        notice = get_notice(notice_id)
        self.session.delete(notice)
        return jsonify({'status': 'deleted'})


notice_view = NoticeView.as_view('user_view')


app.add_url_rule('/notices/<int:notice_id>', view_func=notice_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/notices', view_func=notice_view, methods=['POST'])

if __name__ == '__main__':
    app.run()
