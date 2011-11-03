from flask import Flask
from questionator.routes.router import blueprint
import os


app = Flask(__name__)
app.config.from_pyfile('questionator/settings.cfg')
app.register_blueprint(blueprint)

#set db locations for models
os.environ['MONGODB_HOST'] = app.config['MONGODB_HOST']
os.environ['MONGODB_PORT'] = app.config['MONGODB_PORT']
os.environ['MONGODB_DATABASE'] = app.config['MONGODB_DATABASE']



if __name__ == '__main__':
    app.run(debug=True)
