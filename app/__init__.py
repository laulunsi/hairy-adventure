# coding=utf-8

__author__ = 'luyangsheng'
from flask import Flask
from flask import request, g
from flask.sessions import SessionInterface
from beaker.middleware import SessionMiddleware
import logging

# global server envrionment options
debug = True


# database settings
_DB_URL_FORMAT = "mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s"
_db_config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "db_sys",
}

# other sever options
options = {
    # use md5sum of my name as cookie_secret
    "SECRET_KEY": "3087c29ddaaed0a7671093b3eb00ad4a",
    "DEBUG": debug
}
session_opts = {
    "session.type": "ext:database",
    "session.url": _DB_URL_FORMAT % _db_config,
    "session.lock_dir": "./lock",
}
# 把自己伪装成php。。。这个有点邪恶
session_setting = {
    "key": "PHPSESSIONID",
}

app = Flask(__name__, static_url_path="")
app.config.update(**options)

# logging config
_log_config = {
    "level": logging.DEBUG,
    "format": "[%(asctime)s][%(levelname)s]--%(name)s--:%(message)s",
}
if not debug:
    _log_config['file'] = "hsp_sys.log"
logging.basicConfig(**_log_config)


class BeakerSessionInterface(SessionInterface):

    def open_session(self, _app, _request):
        _session = request.environ['beaker.session']
        return _session

    def save_session(self, _app, _session, response):
        _session.save()


# initial database session before request
@app.before_request
def before_request():
    pass


# close database session after request
@app.teardown_request
def teardnow_request(exception):
    pass

app.wsgi_app = SessionMiddleware(
    app.wsgi_app,
    session_opts,
    **session_setting
)
app.session_interface = BeakerSessionInterface()

from controller import *