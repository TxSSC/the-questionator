import os
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('settings.cfg')
#app.register_blueprint(routes)
import routes.router

#set db locations for models
os.environ['MONGODB_HOST'] = app.config['MONGODB_HOST']
os.environ['MONGODB_PORT'] = app.config['MONGODB_PORT']
os.environ['MONGODB_DATABASE'] = app.config['MONGODB_DATABASE']
