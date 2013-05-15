OpenReader
==========

## What is OpenReader?

OpenReader is an open-source Django app (Only tested on Django 1.5+ so far...) that you can use on your very own site to have your personal clone of Google Reader!

Basically, I was upset that Google Reader was shutting down and didn't like any of the other options, so I decided to take a couple days and build my own. It's designed to be very basic, and I'll be adding more features to it as requested or as I see I need them in my personal use.

Currently, OpenReader uses the Django authentication system in conjunction with Google Authentication, so the login is as easy as Google Reader was.

## Can I see it in action before I build my own?

Sure! I'm hosting an open OpenReader that anyone can sign up for, just head on over to [My Site](http://mooselion.com/reader/)

## How Do I Make My Own?

This section is in progress. Right now, OpenReader is not as customizable as I'd wish, and it's still very much in the alpha stage. The first step, at this point, is to obtain the source code and add it to your pythonpath. Then install all the requirements found in requirements.txt. This step will be simplified once I get the code on PyPI so please bear with me.

Now, with the code installed, you need your own Django project. It'd be nice if you have your own project, but if you need to set one up, head on over [here](https://docs.djangoproject.com/en/dev/intro/tutorial01/).

Next, install the app in your settings.py file. Add these lines:

	#OpenReader settings
	OPENREADER_UNIVERSAL_LOGIN = True # If set to False, you must create manually users with the same emails as the google accounts that are attempting to log in. Otherwise, anyone can create an account on your reader.

	# Open ID required for OpenReader
	AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend','openreader.auth.GoogleBackend',)
	LOGIN_URL = '/reader/login/'
	LOGIN_REDIRECT_URL = '/reader/reader/'
	LOGOUT_URL = '/reader/logout/'
	OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

And also add the app to your Django project:

	INSTALLED_APPS = (
	
		...
	
	    'openreader',
	)

Next, add the url definitions to your urls.py:

	urlpatterns = patterns('',
		
		...
		
	    url(r'^reader/', include('openreader.urls', 'reader/', 'reader')),
	)

With those in place, your reader will work, but it won't know how to automatically pull in the feeds! To do so, create a script with the following, and set it to run every hour or so (please, be polite to your RSS feeds and don't spam them).

	from {PROJECT_NAME} import settings
	from django.core.management import setup_environ
	setup_environ(settings)
	
	from openreader.scripts import read_feeds
	
	read_feeds.read_all()

And you're all set! Fire up your Django project, and point your browser to /reader/ and log in with your Google Account.

## What's next?

The immediate things that need to be added are: more settings options, allowing more log in options than Google, the ability to show feed items you've read, and feed suggestions.