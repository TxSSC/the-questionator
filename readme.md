The Questionator
================
A small flask app built to serve anonymous quiz style questionnaires.

## Running in production
- Change `debug` to `False` in `questionator/config/app_settings.conf`
- Set the correct ***unix socket*** paths in `questionator/config/gunicorn.conf`

## Install
- Navigate to the base repo directory `cd [questionator repo dir]`
- Run the bootstrap if no virtual environment is installed
  - Set the virtual environment name with `export VIRTIAL_ENV=[name]`
  - Then run `./bootstrap -i` to install required packages

## Running
- Activate the virtual environment with `source $VIRTUAL_ENV/bin/activate`
- Start the server with `gunicorn -c questionator/config/gunicorn.conf questionator:app` *This will provide a unix socket endpoint for nginx*
