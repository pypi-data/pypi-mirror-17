======
Proton
======

Proton is a Django module for building desktop apps. It provides a management command
to run the project as a desktop application rather than a server, as well as some
basic starter templates for using various stylesheets.
Behind the scenes, this is done by running the server on an arbitrary high port
and opening a thin web browser pointing to localhost on that port.

Quick Start
-----------

1. Install dependencies:
    Ubuntu: `apt-get install python-gi gir1.2-webkit-3.0 gir1.2-gtk-3.0

2. Add "proton" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'proton',
    ]

3. Add the following values to your settings.py file:

    WINDOW_TITLE = 'Title of window'
    WINDOW_SIZE = (WIDTH, HEIGHT)
    WINDOW_MAXIMIZE = False

WINDOW_SIZE is a tuple containing the default width and height of the window.
WINDOW_MAXIMIZE represents whether the window should be maximized by default.

4. Run `python manage.py window` to run the app locally using the dev server.


