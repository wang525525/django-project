# django-angular project

To be compliant with other libraries such as **djangorestframework**,  server-side responses on
rejected forms use error code 422, rather than 200. If you use your own form controllers, adopt
them accordingly. The JSON format used to communicate errors downstream has changed slightly.

### New Features

For a smoother transition path, **django-angular** added two directives in version 2.0:

``<form djng-endpoint="/path/to/endpoint">...</form>``, which can be used to upload form
data to the server. It also populates the error fields, in case the server rejected some data.

``<djng-forms-set endpoint="/path/to/endpoint"><form ...>...</form>...</djng-forms-set>``
Similar to the above directive, but rather than validating one single form, it validates a
set of forms using one shared endpoint.

A promise chain has been introduced. Buttons used to submit form data and then proceed with
something else, now can be written as:

## Documentation

Detailed documentation on [ReadTheDocs](http://django-angular.readthedocs.org/en/latest/).

[Demo](http://django-angular.awesto.com/form_validation/) on how to combine Django with Angular's form validation.

Please drop me a line, if and where you use this project.


## Features

* Seamless integration of Django forms with AngularJS controllers.
* Client side form validation for Django forms using AngularJS.
* Let an AngularJS controller call methods in a Django view - kind of Javascript RPCs.
* Manage Django URLs for static controller files.
* Three way data binding to connect AngularJS models with a server side message queue.
* Perform basic CRUD operations.

## Future Plans
A next big change to **django-angular** should be to add support for Angular2/4/5.
However, I'm still unsure about the future roadmap of the Angular, and I currently
don't have the resources to do so.

