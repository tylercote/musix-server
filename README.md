## Database Setup:
1. Install MySQL 8 Community: https://dev.mysql.com/downloads/mysql/
2. Install MySQL Workbench (or any other tool to manipulate a MySQL DB): https://dev.mysql.com/downloads/workbench/
3. Follow MySQL set up instructions
4. Create a new database called “MyMusix” using MySQL Workbench


# Backend Setup:
1. Install Python 3.8 and follow the setup instructions.  Choose to include python in PATH when prompted: https://www.python.org/downloads/release/python-380/
2. Create and activate a local python environment in root project folder. Run the following commands:

`python -m venv local_python_env`

`source local_python_env/bin/activate`

3. Navigate to project directory containing requirements.txt
4. Run `python -m pip install -r requirements.txt`

5. Edit settings.py > DATABASES to include the password you chose when setting up MySQL.
6. Run the following commands in the same directory as manage.py

`./manage.py makemigrations`

`./manage.py migrate auth`

`./manage.py migrate --run-syncdb`

`./manage.py createsuperuser` (follow the instructions to set up a user account)

`./manage.py runscript add_festival_artists` (this populates a few festivals, along with the associative table festivals_artists using data found online)

`./manage.py runserver`

Heroku Run Local
python manage.py collectstatic
heroku local web
