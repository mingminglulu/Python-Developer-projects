hypernews/wsgi.py
"""
WSGI config for hypernews project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypernews.settings')

application = get_wsgi_application()
hypernews/__init__.py
hypernews/settings.py
"""
Django settings for hypernews project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NEWS_JSON_PATH = 'news.json'  # You can choose any path you want
NEWS_JSON_PATH = os.environ.get('NEWS_JSON_PATH') or NEWS_JSON_PATH  # DO NOT MODIFY THIS LINE

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(-q5783z2mh-cd217skey@(+_np2&j0=sl6suvo)ah2uwz@9ij'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hypernews.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hypernews.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
manage.py
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypernews.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
news/apps.py
from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'
news/admin.py
from django.contrib import admin

# Register your models here.
news/tests.py
from django.test import TestCase

# Create your tests here.
news/views.py
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.conf import settings
import json
import itertools


def get_json_data():
    json_data = settings.NEWS_JSON_PATH
    with open(json_data, 'r') as f:
        data = json.load(f)
    return data


class ComingSoonView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Coming soon')


# {% regroup articles|dictsortreversed:"created" by created|slice:":-9" as news_list %}
class ArticlesListView(View):
    def get(self, request, *args, **kwargs):
        data = get_json_data()

        sorted_news = sorted(data, key=lambda i: i['created'], reverse=True)
        groupped_news = itertools.groupby(sorted_news, lambda i: i['created'][:10])

        articles = []
        for k, v in groupped_news:
            articles.append((k, list(v)))

        context = {'articles': articles}
        return render(request, 'news/articles.html', context=context)


class ArticleView(View):
    def get(self, request, article_id, *args, **kwargs):
        data = get_json_data()
        article = list(filter(lambda x: x['link'] == int(article_id), data))
        if not article:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        context = {'article': article[0]}
        return render(request, 'news/article.html', context=context)
news/models.py
from django.db import models

# Create your models here.
news/migrations/__init__.py
news/__init__.py
hypernews/urls.py
"""hypernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from news.views import ArticleView, ArticlesListView, ComingSoonView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ComingSoonView.as_view()),
    path('news/', ArticlesListView.as_view()),
    path('news/<slug:article_id>/', ArticleView.as_view())
]
news/templates/news/base.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Hyper News{% endblock %}</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
news/templates/news/articles.html
{% extends 'news/base.html' %}

{% block title %}{{ block.super }}{% endblock %}

{% block content %}
    <h2>Hyper news</h2>
    {% for article in articles %}
        <h4>{{ article.0 }}</h4>
            <ul>
                {% for a in article.1 %}
                    <li><a href="/news/{{ a.link }}/">{{ a.title }}</a></li>
                {% endfor %}
            </ul>
    {% endfor %}
    <a href="/news/create/"></a>
{% endblock %}
news/templates/news/article.html
{% extends 'news/base.html' %}

{% block title %}{{ block.super }}{% endblock %}

{% block content %}
    <h2>{{ article.title }}</h2>
    <p>{{ article.created }}</p>
    <p>{{ article.text }}</p>
    <a href="/news/">News</a>
{% endblock %}
hypernews/news.json
[{"created": "2020-02-22 16:40:00", "text": "A new star appeared in the sky.", "title": "A star is born", "link": 9234732}, {"created": "2020-02-09 14:15:10", "text": "Text of the news 1", "title": "News 1", "link": 1}, {"created": "2020-02-10 14:15:10", "text": "Text of the news 2", "title": "News 2", "link": 2}, {"created": "2020-02-09 16:15:10", "text": "Text of the news 3", "title": "News 3", "link": 3}]