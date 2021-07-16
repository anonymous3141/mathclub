# Guide to Software
If you are reading this, you are probably looking to extend my software. Good luck! I highly recommend a good knowledge of python, and basic knowledge of object orientated programming. Javascript can be learnt on the fly (and I still don't know that much CSS). It will take a few days to understand the codebase, so don't be alarmed if it seems very complex. I had to do a lot of googling so there's no shame to it. 

You will find installation instructions and an overview of architecture, but not detailed descriptions. The code should be mostly self descriptive, and some functions and commands will inevitably need research.

## Overview
- The system uses the Django web framework
- It uses python3 as a backend (for database work and serving web pages) and javascript/html/css for the frontend (the webpages themselves)
- It contains a static component and dynamic component. For the static component please see technical details in "Basic Usage Guide"
- The python system is linked by django to an SQL database, and SQL commands are executed from an python API.
### Import sites For learning
- stackoverflow.com 
- w3schools.com
- https://docs.djangoproject.com/en/3.2/
- Github
- Browser web developer tools (the console and breakpoints are very good for debugging javascript)
- Know basic Git I guess

## Cloning the repository for local Testing
Production is another beast with its own article. This section describes how to clone the repository from github for local testing. I will describe the basics of installation (from linux perspective, I haven't done this on windows before, but it should be similar). I think this works, but haven't tried.

1) Using terminal in the Home directory (parent directory of desktop):
```
git clone git@github.com:Maths-Club/mathclub.git
```
note that you should set up SSH first.

2) This should create a folder named github, and you should cd into it.

3) Install pip


4) On command terminal set up virtual environment
```
sudo apt update //get apt installer up to scratch
sudo apt install python3-venv python3-pip //download venv lib
python3 -m venv venv_orac //make venv
source venv_orac/bin/activate //activate venv
```
5) Go to mathclub/settings, set PROD = False, DEBUG=True

6) In Venv pip install the following libraries:
```
pip install django
pip install django-registration-redux
pip install whitenoise
pip install sqlite
```
7) Make migrations and create superuser:
```
python3 manage.py migrate
python3 manage.py makesuperuser //enter credentials as prompted
```
8) Command to run server, which is served at localhost:8000
```
python3 manage.py runserver
```

## Architecture

### Basic introduction to Django
 The Client (the user) communicates with a server with HTTP requests, generally by clicking links on browsers or through the browser webpage interface. The work of our software is to respond to requests and either
 - Perform an action
 - Return and render a webpage
 - Do Both

A HTTPrequest will be directed at a URL, and contain several different pieces of information, such as:
- Username
- Datapacks
- Type, like GET and POST (more on this later)

Django's system is very well designed, and can be divided into 4 sections:
- **URL Handler**, which accepts incoming requests, and based on their URL evokes relevant **view** functions to respond to requests. View reverses are really good practice by the way.  The base URL handler can be extended by sub-handlers using the extend() function.

- **View functions**, are evoked by the URL handler, which takes a HTTPrequest (which appears in python as a HTTPrequest object) with its attached information and returns a **HTTPresponse**, which can be:
	-  a piece of text (when retrieving information from a database)
	-  a redirect to another page
	-  a website page to render. 
	- In the latter case, the django render() function is used, which takes a precoded **template** made up of HTML, javascript, CSS populates it with data determined by the view function (such as the name of the user who made the request), and returns the populated template as a webpage

- **Database:** The File models.py in the db folder contains various models. You can instantiate these models, and store them in a database which can persist and be accessed later. These models can be queried using an SQL like API which can be imported by all view functions

- **Templates**: It is like an ordinary HTML/CSS/JS file except you can use tags like {{ contextName }} and {% for elem in contextArray %} to load in extra stuff supplied to the template by a view Function. The tag system is very intuitive, fortunately. Templates can also inherit other templates by slotting in content using the block tag

### The Folders
**db**
Contains auto-generated migration files as well as models.py, which describe the format of the data which is persisted

**mathclub**
Contains the important settings.py and other files needed for production
Contains the central URL dispatcher. 

**quiz**
Contains a URL dispatcher extension, as well as view functions for quiz listing, rendering and grading

**SABER**
Contains the view functions for the admin interface. SABERcommands.py is the central gateway to which admin database requests and manipulations are handled. 

**Static**
Contains the static files (images, CSS etc, web icon favicon) etc

**Templates**
Contains all the templates which are used by views to render quizs. 

### External dependencies

- Django Registration Redux: takes care of login/logout
- Whitenoise for serving static files in prod

Javascript includes:
- Mathjax: for rendering formulas
- TinyMCE: a rich text editor
- MathLive: a Latex Editor

## Notes From the Author's experience developing

### Get and Post requests
**Get**: faster, simpler query. Good for retrieving information. Normal requests for web pages use get.
**Post**: better for telling the database to do something
- Follow pre-existing code examples for AJAX (aynschronous javascript) requests
### Javascript
- Get comfortable with DOM (what it means etc). It will help developing more complex frontends like the question List interface.
- Know what XML, Json files are
- Most communication is done using Json files between server and client

### Database API
- Get comfortable with basic SQL ideas (like what ForeignKeys and ManyToMany Fields are)
- Get the database to do as much of the work as possible
- python3 manage.py dbshell is really useful for debugging
- .get(), .all(), .filter() are the most frequent functions. querysets function much like arrays
- Migrations aren't that scary. Every time you change models.py do 
```
python3 manage.py makemigrations
python3 manage.py migrate
```

### Python Importing:
- Django treats the home directory of the app as the home directory when importing: e.g in ``from . import lib``, . is the current directory meaning
- Get comfortable with python decorators. They're basically wrappers around the function that slightly modify it.
- Reverse URL matching: ``from django.urls import reverse``
What it does is the identification of the corresponding Django URL from a name given to a view function. This is made possible by the fact that each view function usually corresponds to a single URL link & Name.
# Guide to deploying on Heroku

This is the guide for deploying the App onto Heroku. 

### Limitations of Heroku
- Somewhat bad downtime for database
- only 550 hours a month of uptime (its okay though for all intents and purposes for one timezone only)
- 10000 database rows (by most calculations will last a year before needing to erase all user problem info, which is fine tbh)
- But who cares its free :)))))

### Key differences between localised django testing and deployment
- The database; It is SQLite in local testing, and Heroku Postgres in Production
- Speed: localhost is faster than heroku
- Heroku requires 3 files that localtesting doesn't, it tells Heroku what dependencies to install when deploying:
	- requirements.txt (specify dependencies)
	- runtime.txt (specify version of python)
	- Procfile (note no extension, tells Heroku how to run)
### Key Points
- Heroku allows deploying from a github repo
- For git usage please just google, it is an essential tool in software dev
- I deployed by following the tutorial. It is really good, and following it to the keystroke will suffice (except for linux, but the difference is minimal)
	- https://www.youtube.com/watch?v=kBwhtEIXGII (For getting the thing onto github then onto heroku. IGNORE the git deployment)
	- https://www.youtube.com/watch?v=TFFtDLZnbSs (First half, for integrating Heroku Postgres)

We use the following script to stage all relevant files. It can be stored as bash (linux) or bat (windows) file and ran as necessary. If more sections are added to the codebase, the code must be changed.
```
git add requirements.txt
git add Procfile
git add runtime.txt

git add templates

git add static

cd db
cd migrations
git add *.py
cd ..
git add *.py
cd ..

cd mathclub
git add *.py
cd ..
cd SABER
git add *.py
cd ..

cd views
git add *.py
cd ..

cd quiz
git add *.py
cd quizUtility
git add *.py
cd ..
cd ..
```

### Procedure for deployment

1) Operate in virtual environment. I assume you created a virtual environment to install django and dependencies.
2) pip install gunicorn, whitenoise (BE IN VENV) These are required packages for production, and are useful to have in local testing. Gunicorn is like the server stack, and whitenoise serves to destribute static (e.g images, immutable files) content

3) snap install heroku (linux) OR download the heroku CLI (windows)

4) Create requirements.txt. Enter the following into command line
```
pip freeze > requirements.txt (dump pip dependencies into requirments.txt
```

It should have stuff like
```
asgiref==3.3.1
confusable-homoglyphs==3.2.0
Django==3.1.7
django-registration-redux==2.9
gunicorn==20.1.0
pytz==2021.1
sqlparse==0.4.1
whitenoise==5.2.0
psycopg2==2.8.5
dj-database-url==0.5.0
```
5) Create Runtime.txt: it specify version of python. A file with content like below should suffice
```
python-3.7.8
```

6) Create Procfile. It has No extension, it is the thing that's ran when the website is built in the heroku VM. The following should do:
```
web: gunicorn mathclub.wsgi --log-file - 
```
7) Settings.py must be adjusted
- It is best if a PROD variable is defined, and when it is set to False produces original local testing settings rather than the modifications
- Probably best to turn DEBUG off for security. If alpha testing no need I guess
- toggle allowed_host to include localhost 127.0.0.1 AND localhost AND https://cgsmathclub.herokuapp.com/ the prod website
- Add whiteNoise middleWare to middleware variable. The position should be just below security. screw with collectStatic. Add the line
```
if PROD:
	STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```


8) Commit to github repo using aforementioned script your whole app (don't include pycache OR wierd files, DO include migration files)
9) Toggle Heroku
- toggle buildpack to python. This is so Heroku knows your app is python
- sync github repo and deploy via manual deploy

10) Toggle Database. Thus far it should be the case that Database stuff doesn't work. By some miracle I don't understand the library dj-database-url does the job;
	- Pip install dj-database-url
	- Add it to requirements.txt
	- Do something like
```
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}
} //default sqlite database

if PROD:
	#modify database
	import dj_database_url
	db_from_env = dj_database_url.config(conn_max_age=600) #from youtube
	DATABASES['default'].update(db_from_env)
```
11) Finally use heroku CLI to update database.
	- Execute commands
	-  Heroku login, follow directions given. Enter your Heroku credentials
	- heroku git:remote -a cgsmathclub (add as remote, replace with your own webname if needed if you are cloning somewhere else)
	- heroku run python3 manage.py migrate //execute migrations on heroku VM
	- If no superusers have been created; do
		- heroku run python3 manage.py createsuperuser
		- Enter your desired credentials and you are good
