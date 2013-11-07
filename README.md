Glucose Tracker
===============

A simple web application for keeping tracking of blood glucose levels.  Written in Python using the Django framework.

This project is currently still in early development.  The goal is to implement the following features:

* Simple, easy to use. Entering glucose data should be faster than finding a pen and paper and writing down the number.  Fields should have pre-set values where it makes sense (such as the date, time, and category based on time of day).
* Send glucose data via email.  Email it to your doctor before your visit, no more carrying log books!  Can be sent as an attachment or including in the email as an HTML table.
* Reports.  Simple reports to see trends on how your diabetes is doing.  Highlight how many times you have lows and highs.
* Data filtering.  Should be easy to filter the table by columns (specify glucose range, date range, category, search notes).
* A1C estimate.  Estimate A1C based on values from the last 3 months.


3rd-Party Apps/Libraries/Plugins
--------------------------------

GlucoseTracker uses the following:

* Twitter Bootstrap 3 (getbootstrap.com)
* Datatables (datatables.net)
* South
* Django-Crispy-Forms
* Django-Braces
* Bootstrap-DateTimePicker
