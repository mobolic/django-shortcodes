# django-shortcodes

This package provides [WordPress
shortcode](http://en.support.wordpress.com/shortcodes/) support for Django
templates. It is based on code by [Mark Steadman](http://marksteadman.com/).

## Installation

Use `pip install django-shortcodes` or clone the [Git
repository](https://github.com/martey/django-shortcodes).

## Usage

    {% load shortcodes_filters %}
    {{ text|shortcodes|safe }}
