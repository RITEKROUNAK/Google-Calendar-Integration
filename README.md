# Google Calendar Integration

This repository houses a Django REST API that enables seamless integration with Google Calendar. The API offers two endpoints specifically designed to handle the authentication process with Google.

Endpoints:

1. `/rest/v1/calendar/init/` - `GoogleCalendarInitView()`
   This endpoint initiates the OAuth process by prompting the user for their credentials. It serves as the first step of the authentication flow.

2. `/rest/v1/calendar/redirect/` - `GoogleCalendarRedirectView()`
   This endpoint handles the redirect request sent by Google after the user grants permission. It performs two tasks:
   a) Retrieves the access token from the provided authorization code.
   b) Once the access token is obtained, it fetches the list of events from the user's Google Calendar.

To ensure secure integration, the API leverages the OAuth2 mechanism, utilizing Google's provided standard libraries. The API strictly adheres to the Django framework and does not rely on any third-party libraries other than the ones provided by Google.

Deployed Link : [Replit](https://replit.com/@ritekrounak/Google-Calendar-Integration)

![image](https://github.com/RITEKROUNAK/Google-Calendar-Integration/assets/64047505/ebfd00de-d8f8-418b-8100-9ba27132b6d7)


# Usage

### Existing virtualenv

If your project is already in an existing python3 virtualenv first install django by running

    $ pip install django
    
And then run the `django-admin.py` command to start the new project:

    $ django-admin.py startproject projectname
      
### No virtualenv

This assumes that `python3` is linked to valid installation of python 3 and that `pip` is installed and `pip3`is valid
for installing python 3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.

If you don't have django installed for python 3 then run:

    $ pip3 install django
    
And then:

    $ python3 -m django startproject projectname
      
      
After that just install the local dependencies, run migrations, and start the server.


# {{ Google Calendar Integration }}

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com:RITEKROUNAK/Google-Calendar-Integration.git
    $ cd Google-Calendar-Integration
    $ cd calender-integration
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py makemigrations
    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
