import os

from questionator import app

if __name__ == '__main__':
    port = os.environ.get('PORT', 3000)
    app.run(host='127.0.0.1', port=int(port))
