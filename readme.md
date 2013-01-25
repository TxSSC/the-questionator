The Questionator
================
A small flask app built to serv anonymous quiz style questionnaires.

## Running in production
- Change `debug` to `False` in `questionator/config/app_settings.conf`
- Set the correct `unix socket` paths in `questionator/config/gunicorn.conf`

```
./bootstrap.py
cd [the-questionator]
source venv/bin/activate
gunicorn -c questionator/config/gunicorn.conf questionator:app
```
