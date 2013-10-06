#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Will Ross'
SITENAME = u'Disaster Area'
SITEURL = ''

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = u'%d %B %Y'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

# Extract the date slug from the file name
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

# Use Markdown for content
MARKUP = ('markdown', 'mdown', 'md')

# Use Typogrify
TYPOGRIFY = True

# Set URLs and paths
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'
# Only process indicies and archives right now
DIRECT_TEMPLATES = ( 'index', 'archives' )

# Show Archives for years and months
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
