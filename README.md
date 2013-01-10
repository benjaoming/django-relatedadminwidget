django-relatedadminwidget
=========================

Widget for displaying edit and delete links alongside foreign key admin widgets

![Flowers](https://github.com/benjaoming/django-relatedadminwidget/raw/master/screenshot.png)

Also see this project: [django-admin-enhancer](https://github.com/charettes/django-admin-enhancer)

Installation:

1. **pip install git+git://github.com/benjaoming/django-relatedadminwidget.git**
2. Add "relatedwidget" to settings.INSTALLED_APPS
3. You may want to run your project's ./manage.py collectstatic
4. In your applications' admin.py, let the model admins inherit from RelatedWidgetWrapperBase like in this example:

    from django.contrib import admin
    from relatedwidget import RelatedWidgetWrapperBase

    class MyModelAdmin(RelatedWidgetWrapperBase, admin.ModelAdmin):
        pass
    
    admin.site.register(MyModel, MyModelAdmin)

It also works with TabularInline and StackedInline! Remember the order of inheritence, always put RelatedWidgetWrapperBase first!

Troubleshooting
---------------

If you get a `TemplateDoesNotExist` error on 'relatedwidget/widget.html', you might have to add `django.template.loaders.eggs.Loader` to your `settings.TEMPLATE_LOADERS`.

Credits
-------

User [nasp](http://djangosnippets.org/users/nasp/) did most of the work, I just updated it for Django 1.4 and packed it as an app.
