# cs412-django

To create a new app you do 

1. python manage.py startapp 'name'
2. Add it to cs412/settings.py
4. Add a 'name'/urls.py file in the app
5. Edit the cs412/urls.py to add the new app
6. Create basic view in 'name'/views.py
7. To run the app:
First: Start django shell if not already started
pipenv shell

Second: Start dev server in django directory
python manage.py runserver
