set-o errexit
pip install requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput