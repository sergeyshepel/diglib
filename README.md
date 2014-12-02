diglib
======

Books library

---------------------------------------------------------------------------

To run app:

cd ./diglib

pip install virtualenv

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt (remove from requirements psycopg2==2.5.1)

python manage.py deploy (to generate database content and tables)

gunicorn manage:app

login:admin 

password:admin

---------------------------------------------------------------------------

To deploy on heroky:

make git repository

heroku login

heroku create diglib

heroku addons:add heroku-postgresql:dev

heroku pg:promote HEROKU_POSTGRESQL_BROWN_URL (color of db will be differ)

heroku config:set FLASK_CONFIG=heroku

git push heroku master

heroku run python manage.py deploy

heroku restart
