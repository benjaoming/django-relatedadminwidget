from django.conf import settings
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.forms.widgets import SelectMultiple
from django.http import HttpResponse
from django.utils.html import escape, escapejs

class RelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    
    class Media:
        js = ("%srelatedwidget/js/relatedwidget.js" % settings.STATIC_URL,)
    
    def __init__(self, *args, **kwargs):
        self.can_change_related = kwargs.pop('can_change_related', None)
        self.can_delete_related = kwargs.pop('can_delete_related', None)
        super(RelatedFieldWidgetWrapper, self).__init__(*args, **kwargs)
    
    @classmethod
    def from_contrib_wrapper(cls, wrapper, can_change_related, can_delete_related):
        return cls(wrapper.widget, wrapper.rel, wrapper.admin_site,
                   can_add_related=wrapper.can_add_related,
                   can_change_related=can_change_related,
                   can_delete_related=can_delete_related)
    
    def get_related_url(self, rel_to, info, action, args=[]):
        return reverse("admin:%s_%s_%s" % (info + (action,)), current_app=self.admin_site.name, args=args)
    
    def render(self, name, value, attrs={}, *args, **kwargs):
        rel_to = self.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        self.widget.choices = self.choices
        attrs['class'] = ' '.join((attrs.get('class', ''), 'related-widget-wrapper'))
        context = {'widget': self.widget.render(name, value, attrs, *args, **kwargs),
                   'name': name,
                   'STATIC_URL': settings.STATIC_URL,
                   'can_change_related': self.can_change_related,
                   'can_add_related': self.can_add_related,
                   'can_delete_related': self.can_delete_related}
        if self.can_change_related:
            if value:
                context['change_url'] = self.get_related_url(rel_to, info, 'change', [value])
            template = self.get_related_url(rel_to, info, 'change', ['%s'])
            context.update({
                            'change_url_template': template,
                            'change_help_text': _('Change related model')
                            })
        if self.can_add_related:
            context.update({
                            'add_url': self.get_related_url(rel_to, info, 'add'),
                            'add_help_text': _('Add Another')
                            })
        if self.can_delete_related:
            if value:
                context['delete_url'] = self.get_related_url(rel_to, info, 'delete', [value])
            template = self.get_related_url(rel_to, info, 'delete', ['%s'])
            context.update({
                            'delete_url_template': template,
                            'delete_help_text': _('Delete related model')
                            })
        
        return mark_safe(render_to_string('relatedwidget/widget.html', context))
    
    
class RelatedWidgetWrapperBase(object):

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(RelatedWidgetWrapperBase, self).formfield_for_dbfield(db_field, **kwargs)
        if (formfield and
            isinstance(formfield.widget, admin.widgets.RelatedFieldWidgetWrapper) and
            not isinstance(formfield.widget.widget, SelectMultiple)):
            request = kwargs.pop('request', None)
            related_modeladmin = self.admin_site._registry.get(db_field.rel.to)
            can_change_related = bool(related_modeladmin and
                                      related_modeladmin.has_change_permission(request))
            can_delete_related = bool(related_modeladmin and
                                      related_modeladmin.has_delete_permission(request))
            widget = RelatedFieldWidgetWrapper.from_contrib_wrapper(formfield.widget,
                                                                    can_change_related,
                                                                    can_delete_related)
            formfield.widget = widget
        return formfield

    def response_change(self, request, obj):
        if '_popup' in request.REQUEST:
            pk_value = obj._get_pk_val()
            return HttpResponse('<script type="text/javascript">opener.dismissEditRelatedPopup(window, "%s", "%s");</script>' % \
            # escape() calls force_unicode.
            (escape(pk_value), escapejs(obj)))
        else:
            return super(RelatedWidgetWrapperBase, self).response_change(request, obj)

class RelatedWidgetWrapperAdmin(admin.ModelAdmin, RelatedWidgetWrapperBase):
    pass

class RelatedWidgetWrapperTabularInline(RelatedWidgetWrapperBase, admin.TabularInline):
    pass

class RelatedWidgetWrapperStackedInline(admin.StackedInline, RelatedWidgetWrapperBase):
    pass
