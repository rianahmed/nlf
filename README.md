# NLF - North South Lost & Found

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/rianahmed/lost_and_found.git
    $ cd lost_and_found/
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply run below command to static file generation

    $ python manage.py collectstatic
    
Then run below command to apply the migrations:

    $ python manage.py makemigerations
    $ python manage.py migrate
    
You can now run the development server:

    $ python manage.py runserver
