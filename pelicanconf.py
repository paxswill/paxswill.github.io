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
LINKS = (('Tutorials', SITEURL + '/tutorials'),
         ('Archives', SITEURL + '/archives'),
        )

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 3

# Extract the date slug from the file name
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

# Use Markdown for content
MARKUP = ('markdown', 'mdown', 'md', 'ipynb')

# Use Typogrify
TYPOGRIFY = True

# Setup plugins
PLUGIN_PATH = 'plugins'
PLUGINS = ['pelican-ipythonnb',]

# Set URLs and paths
ARTICLE_DIR = 'blog'
ARTICLE_URL = 'blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'
PAGE_DIR = ''
PAGE_EXCLUDES = ('blog', )
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'

# Static resources
STATIC_PATHS = [
        'CNAME',
        '.travis.yml',
    ]

# Disable tag, category and author pages
CATEGORY_SAVE_AS = False
TAG_SAVE_AS = False
TAGS_SAVE_AS = False
AUTHOR_SAVE_AS = False
AUTHORS_SAVE_AS = False

# Only process indicies and archives right now
DIRECT_TEMPLATES = ( 'index', 'archives' )

# Show Archives for years and months
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme config
THEME = 'disaster-theme'

# Social stuff
SOCIAL = (
        ('email', 'paxswill@paxswill.com'),
        ('github', 'paxswill'),
        ('atom', True),
    )
