Django-Reamaze
==================

Django Reamaze is django app for integrate Reamaze ( http://reamaze.com ) LightBox in django project.

It's tested with django 1.4(py2.7) and 1.8(py2.7 and py3.4)

[![Build Status](https://travis-ci.org/mrjmad/django-reamaze.svg?branch=master)](https://travis-ci.org/mrjmad/django-reamaze)  [![Coverage Status](https://img.shields.io/coveralls/mrjmad/django-reamaze.svg)](https://coveralls.io/r/mrjmad/django-reamaze?branch=master)

USAGE
======

you need populate this value in settings.py : 

* REAMAZE_SECRET_KEY (your SSO Key, in settings of Reamaze)
* REAMAZE_JS_URL (in  Website Integration / Support Lightbox of Reamaze)
* REAMAZE_ACCOUNT (name of reamaze account)
* REAMAZE_CHANNEL  (mailbox for messages)
* REAMAZE_OK_FOR_ANONYMOUS (only for you authentified django user or for everyone ?)
* REAMAZE_PREFIX_USER_ID if you will use a prefix before django user id.
