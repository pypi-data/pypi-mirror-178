# Django Vanillaframework
[![CI](https://github.com/lvoytek/django-vanillaframework/actions/workflows/ci.yml/badge.svg)](https://github.com/lvoytek/django-vanillaframework/actions/workflows/ci.yml)

[Vanilla Framework](https://vanillaframework.io/) frontend for Django

## Requirements
Python 3.6 or newer, [Django](https://www.djangoproject.com/) 3.2 or newer

## Install
### Using pip:

```bash
pip install django-vanillaframework
```

## Setup
Add `'vanillaframework'` to the `INSTALLED_APPS` list in your project settings
```python
INSTALLED_APPS = [
    ...,
    'vanillaframework'
]
```

At this point, you can use Vanilla Framework in your Django templates, and the css will be pulled from [assets.ubuntu.com](https://assets.ubuntu.com/v1/vanilla-framework-version-3.8.2.min.css)

If you would like to use a local copy of the css file, run the install management command:

```bash
python3 manage.py vanillaframework -i --css
```

The vanillaframework_css tag will grab the local file from now on until it is deleted.

If you would like to customize Vanilla Framework settings, you can instead install the source sass files. Make sure `npm` is installed on your system before you begin.

Run the installer without the --css argument:

```bash
python3 manage.py vanillaframework -i
```

This will install the npm vanilla-framework package to the static folder alongside the file `vanillaframework.scss`. Use this file to customize the library.

Note: If you are using the sass version of Vanilla Framework, you will have to install `django-compressor` and a sass compiler such as `django-libsass` then update your settings file accordingly:

```python
INSTALLED_APPS = [
    ...,
    'django.contrib.staticfiles',
    'vanillaframework',
    'compressor'
]

STATICFILES_FINDERS = (
    ...,
    'compressor.finders.CompressorFinder'
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
```

## Usage
Once django-vanillaframework is set up, you can use it by including the relevant tags in a Django template.

For the css version, use `vanillaframework_css`:

```jinja2
{% load vanillaframework_tags %}

<html>
    <head>
        {% vanillaframework_css %}
    </head>
</html>
```

And for the sass version, use `vanillaframework_sass`:

```jinja2
{% load vanillaframework_tags %}

<html>
    <head>
        {% vanillaframework_sass %}
    </head>
</html>
```

Vanilla Framework can now be used in the same way it would be with a nodejs project. For information on this syntax, see the [Vanilla Framework website](https://vanillaframework.io/docs).