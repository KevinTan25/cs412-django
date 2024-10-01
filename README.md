# cs412-django

To create a new app you do 

1. python manage.py startapp 'name'

(Steps 2 and 3 are all we need for the global cs412 directory)
2. Add it to cs412/settings.py
3. Edit the cs412/urls.py to add the new app

4. Add a 'name'/urls.py file in the app
5. Create basic view in 'name'/views.py
6. To run the app:
First: Start django shell if not already started
pipenv shell

Second: Start dev server in django directory
python manage.py runserver


To Run Heroku:
(Might need to create another app in heroku and connect it to github)
-1: Create app on heroku
0: heroku git:remote -a 'app_name_in_heroku'

1. git push heroku main
2. heroku ps:scale web=1
3. heroku open
4. Stop the app at the end: heroku ps:scale web=0


To build the database
1. Change your models.py to include your database models
2. python manage.py makemigrations 'name' (If we ever change the data attributes we have run this command. WILL BE ON QUIZ)
3. python manage.py migrate
4. (Need to create superuser if forgot password with python manage.py createsuperuser)
5. python manage.py runserver and go to /admin/
6. Modify 'name'/admin.py
7. Press add on the website next to the name under your app and add your data (This data will be stored in db.sqlite)
8. Write web app to display data
