pip install -r requirements_test.txt --use-mirrors
sudo start xvfb &
python manage.py test

