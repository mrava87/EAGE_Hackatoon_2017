It's not our FAULT! website
============================

This folder/repo contains the Django+frontend code to run the website.

Instructions
------------

To run a local copy, first make sure you have the requirements. You can do this with:

    pip install -r requirements.txt
    
Make sure you are running Python 2.7. Then, simply run the local server with

    python2.7 manage.py runserver
    
You should then be able to access the website on ``http://127.0.0.1:8000/``

For quick sharing, you can tunnel your network traffic and obtain a URL which can be accessed from outside your local network using [ngrok](https://ngrok.com/download).
Simply fire up your local server, and then run:

    /path/to/ngrok http 8000
