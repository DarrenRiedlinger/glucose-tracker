Glucose Tracker
===============

A simple web application for keeping tracking of blood glucose levels.  Written in Python using the Django framework.

This project is currently still in early development.  The goal is to implement the following features:

* <b>Simple, easy to use.</b>  Entering glucose data should be faster than finding a pen and paper and writing down the number.  Fields should have pre-set values where it makes sense (such as the date, time, and category based on time of day).
* <b>Send glucose data via email.</b>  Email it to your doctor before your visit, no more carrying log books!  Can be sent as an attachment or including in the email as an HTML table.
* <b>Reporting.</b>  Simple reports to see trends on how your diabetes is doing.  Highlight how many times you have lows and highs.
* <b>Data filtering.</b>  Should be easy to filter the table by columns (specify glucose range, date range, category, search notes).
* <b>A1C estimation.</b>  Estimate A1C based on data from the last 3 months.
* <b>Mobile friendly.</b>  You should be able to use the app wherever you are and should still be easy to use and readable.

Live Demo
---------

I'm still working on deployment, but the main website will be located at: http://www.glucosetracker.net

The demo/dev website (automated nightly builds) will be set to: http://dev.glucosetracker.net

3rd-Party Apps/Libraries/Plugins
--------------------------------

GlucoseTracker uses the following:

* Twitter Bootstrap 3 (http://getbootstrap.com)
* Datatables (http://datatables.net)
* South (http://south.aeracode.org)
* Django-Crispy-Forms (http://django-crispy-forms.readthedocs.org/en/latest)
* Django-Braces (http://django-braces.readthedocs.org/en/v1.2.2/)
* Bootstrap-DateTimePicker (http://eonasdan.github.io/bootstrap-datetimepicker/)
