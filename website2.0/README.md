# It's not our FAULT! website

## version 2.0

This folder contains the Django+frontend code to run the website (2.0). Changes with respect to version 1:

* Submissions are stored in a database.

* The django project is configured for deployment to Amazon's Elastic Beanstalk service (roughly following instructions in [this blogpost](https://realpython.com/blog/python/deploying-a-django-app-to-aws-elastic-beanstalk/)).

* The opencv-python package is not available on the AWS repos so has been removed from the requirements. It can be built on the server e.g. following [this workflow](https://stackoverflow.com/a/38867965).

* To run the site locally the following variables should be made available in the environment: ADMIN_PASW, KEYSPACE, SECRET_KEY. Remotely (on AWS' Elastic Beanstalk) also AWS_SECRET_ACCESS_KEY.

* The [Elastic Beanstalk command line interface](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html) integrates with git to know which version to deploy to the server. Therefore this folder by itself is under git control. 


## version 1

### Instructions

To run a local copy, first make sure you have the requirements. You can do this with:

    pip install -r requirements.txt
    
Make sure you are running Python 2.7. Then, simply run the local server with

    python2.7 manage.py runserver
    
You should then be able to access the website on ``http://127.0.0.1:8000/``

For quick sharing, you can tunnel your network traffic and obtain a URL which can be accessed from outside your local network using [ngrok](https://ngrok.com/download).
Simply fire up your local server, and then run:

    /path/to/ngrok http 8000
