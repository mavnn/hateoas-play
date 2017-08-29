# A HATEOAS django backend with angular 2.0 UI

Purely for experimentation, with minimal error handling and no styling whatsoever.

It looks like this:

![animated demo](./demo.gif)

(So basically crud, but with no delete or update. Or Cr, as I like to call it)

The main thing of interest is the fact that only the root api url is hardcoded into angular;
all other urls are via links returned, and all identifiers are UUIDs making url guessing impossible.
