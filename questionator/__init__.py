import os
from flask import Flask
from questionator.lib.tools import url_for_page

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
app.jinja_env.globals['url_for_page'] = url_for_page
#import all the routes/controller
import routes.router

#set db locations for models
os.environ['MONGODB_HOST'] = app.config['MONGODB_HOST']
os.environ['MONGODB_PORT'] = app.config['MONGODB_PORT']
os.environ['MONGODB_DATABASE'] = app.config['MONGODB_DATABASE']
