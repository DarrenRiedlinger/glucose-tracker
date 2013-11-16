Glucose Tracker
===============

.. image:: https://travis-ci.org/jcalazan/glucose-tracker.png
    :target: https://travis-ci.org/jcalazan/glucose-tracker

A simple web application for keeping tracking of blood glucose levels.  Written in Python using the Django framework.

This project is currently still in early development.  The goal is to implement the following features:

* <b>Simple, easy to use.</b>  Entering glucose data should be faster than finding a pen and paper and writing down the number.  Fields should have pre-set values where it makes sense (such as the date, time, and category based on time of day).
* <b>Send glucose data via email.</b>  Email it to your doctor before your visit, no more carrying log books!  Can be sent as an attachment or included in the email as an HTML table.
* <b>Reporting.</b>  Simple reports to see trends on how your diabetes is doing.  Highlight how many times you have lows and highs.
* <b>Data filtering.</b>  Should be easy to filter the table by columns (specify glucose range, date range, category, search notes).
* <b>A1C estimation.</b>  Estimate A1C based on data from the last 3 months.
* <b>Mobile friendly.</b>  You should be able to use the app wherever you are and should still be easy to use and readable.

<b>To Do List:</b> https://trello.com/c/ZN9ualI3

Installation/Running the App
----------------------------

1. Change the settings/local.py file to match your environment (I'll create a demo.py file later that uses SQLite so you won't have to set up your own database).
2. Install the required libraries listed in the requirements file with pip: pip install -r requirements.txt
3. Run the local web server: python manage.py runserver --settings=settings.local

Live Demo
---------

To show the progress of the app, a live demo is available at: http://demo.glucosetracker.net

This project uses Travis CI to auto-deploy the latest code from the master to the demo site on git push.

3rd-Party Apps/Libraries/Plugins
--------------------------------

GlucoseTracker uses the following:

* Twitter Bootstrap 3 (http://getbootstrap.com)
* Datatables (http://datatables.net)
* South (http://south.aeracode.org)
* Django-Crispy-Forms (http://django-crispy-forms.readthedocs.org/en/latest)
* Django-Braces (http://django-braces.readthedocs.org/en/v1.2.2/)
* Bootstrap-DateTimePicker (http://eonasdan.github.io/bootstrap-datetimepicker/)
