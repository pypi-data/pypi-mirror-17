=== Seo-Meow ===

Seo-Meow is a very simple Django app to manage basic SEO tags.

Installation
------------

::

    $ pip install git+https://github.com/utekay/seo-meow.git

::

    # settings.py

    INSTALLED_APPS = [
        ...
        'seomeow',
    ]

::

    $ python manage.py migrate seomeow

Usage
~~~~~

The app looks for the SeoMeow object that matches the current URL.
Otherwise it returns the object for “/” which is created automatically.

::

    {% load seomeow %}

    <!DOCTYPE html>
    <html lang="en">
      <head>
        ...
        {% put_seo_meow_tags_here %}
        ...

Also you can ‘assign’ the SeoMeow object to any model instance via
Django admin interface. A hyperlink for editing or creating a related
SeoMeow object will be available in the message area after mixin class
is added to the admin model.

::

    # admin.py

    from django.contrib import admin
    from seomeow.admin import SeoMeowShortcut

    from .models import News

    @admin.register(News)
    class NewsAdmin(SeoMeowShortcut, admin.ModelAdmin):
        ...

The model method “get\_absolute\_url” is required in this case.

::

    # models.py

    from django.db import models
    from django.core.urlresolvers import reverse

    class News(models.Model):
        ...

        def get_absolute_url(self):
            # return "/news/%d/" % self.pk # or
            return reverse("news", args=(self.pk,))
