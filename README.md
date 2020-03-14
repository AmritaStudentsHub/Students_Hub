# Students_Hub
Software Engineering Project
Commands to make locally in your system:
mkdir Students_Hub
cd Students_Hub
virtualenv new
source new/bin/activate
pip install Django==2.2.10
django-admin startproject students .
python3 manage.py migrate
python manage.py startapp login
git init
git remote add origin https://github.com/AmritaStudentsHub/Students_Hub.git
git fetch origin master
git reset --hard origin/master
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
