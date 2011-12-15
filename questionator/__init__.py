import os
from flask import Flask, session
from questionator.lib.tools import url_for_page

app = Flask(__name__)
app.config.from_pyfile('config/app_settings.conf')
app.jinja_env.globals['url_for_page'] = url_for_page
app.jinja_env.globals['session'] = session


if not app.debug:
    import logging
    from logging import FileHandler, Formatter
    handler = FileHandler('shared/questionator.error.log', mode='a')
    log_format = Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(log_format)
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)

#import all the routes/controller
import routes.router

#set db locations for models
os.environ['MONGODB_HOST'] = app.config['MONGODB_HOST']
os.environ['MONGODB_PORT'] = app.config['MONGODB_PORT']
os.environ['MONGODB_DATABASE'] = app.config['MONGODB_DATABASE']
