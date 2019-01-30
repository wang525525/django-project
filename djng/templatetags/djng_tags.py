# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json

from django.template import Library
from django.template.base import Node, NodeList, TextNode, VariableNode
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_from_request

from djng.core.urlresolvers import get_all_remote_methods, get_current_remote_methods


register = Library()


@register.simple_tag(name='djng_all_rmi')
def djng_all_rmi():
    """
    Returns a dictionary of all methods for all Views available for this project, marked with the
    ``@allow_remote_invocation`` decorator. The return string can be used directly to initialize
    the AngularJS provider, such as ``djangoRMIProvider.configure({­% djng_rmi_configs %­});``
    """
    return mark_safe(json.dumps(get_all_remote_methods()))


@register.simple_tag(name='djng_current_rmi', takes_context=True)
def djng_current_rmi(context):
    """
    Returns a dictionary of all methods for the current View of this request, marked with the
    @allow_remote_invocation decorator. The return string can be used directly to initialize
    the AngularJS provider, such as ``djangoRMIProvider.configure({­% djng_current_rmi %­});``
    """
    return mark_safe(json.dumps(get_current_remote_methods(context.get('view'))))


@register.simple_tag(name='load_djng_urls', takes_context=True)
def djng_urls(context, *namespaces):
    raise DeprecationWarning(
        "load_djng_urls templatetag is deprecated and has been removed from this version of django-angular."
        "Please refer to documentation for updated way to manage django urls in angular.")


class AngularJsNode(Node):
    def __init__(self, django_nodelist, angular_nodelist, variable):
        self.django_nodelist = django_nodelist
        self.angular_nodelist = angular_nodelist
        self.variable = variable

    def render(self, context):
        if self.variable.resolve(context):
            return self.angular_nodelist.render(context)
        return self.django_nodelist.render(context)


@register.tag
def angularjs(parser, token):
    """
    Conditionally switch between AngularJS and Django variable expansion for ``{{`` and ``}}``
    keeping Django's expansion for ``{%`` and ``%}``

    Usage::

        {% angularjs 1 %} or simply {% angularjs %}
            {% process variables through the AngularJS template engine %}
        {% endangularjs %}

        {% angularjs 0 %}
            {% process variables through the Django template engine %}
        {% endangularjs %}

        Instead of 0 and 1, it is possible to use a context variable.
    """
    bits = token.contents.split()
    if len(bits) < 2:
        bits.append('1')
    values = [parser.compile_filter(bit) for bit in bits[1:]]
    django_nodelist = parser.parse(('endangularjs',))
    angular_nodelist = NodeList()
    for node in django_nodelist:
        # convert all occurrences of VariableNode into a TextNode using the
        # AngularJS double curly bracket notation
        if isinstance(node, VariableNode):
            # convert Django's array notation into JS array notation
            tokens = node.filter_expression.token.split('.')
            token = tokens[0]
            for part in tokens[1:]:
                if part.isdigit():
                    token += '[%s]' % part
                else:
                    token += '.%s' % part
            node = TextNode('{{ %s }}' % token)
        angular_nodelist.append(node)
    parser.delete_first_token()
    return AngularJsNode(django_nodelist, angular_nodelist, values[0])


@register.simple_tag(name='djng_locale_script', takes_context=True)
def djng_locale_script(context, default_language='en'):
    """
    Returns a script tag for including the proper locale script in any HTML page.
    This tag determines the current language with its locale.

    Usage:
        <script src="{% static 'node_modules/angular-i18n/' %}{% djng_locale_script %}"></script>
    or, if used with a default language:
        <script src="{% static 'node_modules/angular-i18n/' %}{% djng_locale_script 'de' %}"></script>
    """
    language = get_language_from_request(context['request'])
    if not language:
        language = default_language
    return format_html('angular-locale_{}.js', language.lower())
