# django-reactjs #
A simple templatetag to load reactjs libraries.

## install ##
Just include `reactjs` into your `INSTALLED_APPS`
```
#!python

INSTALLED_APPS += [ "reactjs" ]
```


## templatetag ##

Load the templatetag
```
#!html
{% load reactjs %}
```

### reactjs ###
Include the reactjs file(s) as `<scrip...></script>` tag(s).
```
#!html
{% reactjs %}
```

### reactjs-with-addons ###
Include the reactjs-with-addons file(s) as `<scrip...></script>` tag(s).
```
#!html
{% reactjs-with-addons %}
```

### CHANGES ###

0.4.0
=====

* renamed reactjs.apps.Config to reactjs.apps.ReactJSConfig
* update to reactjs 15.3.1
* removed python2 support


