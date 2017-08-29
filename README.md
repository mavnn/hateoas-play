# A HATEOAS django backend with angular 2.0 UI

Purely for experimentation, with minimal error handling and no styling whatsoever.

It looks like this:

![animated demo](./demo.gif)

(So basically crud, but with no delete or update. Or Cr, as I like to call it)

The main thing of interest is the fact that only the root api url is hardcoded into angular;
all other urls are via links returned, and all identifiers are UUIDs making url guessing impossible.

## Want to spin it up yourself?

You'll need to have a Python env set up with the items in requires.txt installed, and have done an npm restore for
angular.

After that, create yourself a django superuser (```python testsite/manage.py createsuperuser```).

Then run ```foreman start all```, wait a moment for angular and browse to ```http://localhost:8000``` where django
will serve everything up for you. Both angular and django will watch for changes and recompile as needed.
