# coding: utf-8
import json
from datetime import datetime, timedelta
from django import template
import sqlparse
from fractions import Fraction

register = template.Library()


@register.simple_tag
def method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)



@register.filter('method')
def method(obj, *args):
    method_name = args[0]
    method = getattr(obj, method_name)
    return method(*args[1:])



@register.filter('ratio')
def ratio(nb, total):
    res = round((nb * 100 / total ), 2)
    return "{}%".format(res)


@register.filter('addition')
def addition(a, b):
    return  round(a+b, 2)



@register.filter('taux')
def taux(a, b):
    return int(round(((a or 0) / ((a or 0) + (b or 0))) * 100, 2)) if (a or 0) + (b or 0) > 0 else 0


@register.filter('moyenne')
def moyenne(a, b):
    return  round(((a or 0) + (b or 0)) / 2, 2)

    
@register.filter('eval')
def eavl(a):
    return eval(a)


@register.filter('couleur')
def couleur(number):
    number = 0 if number == '' else number
    if number > 2.5:
        return "primary"
    elif number > 2:
        return "info"
    elif number > 1.5:
        return "success"
    elif number > 1:
        return "warning"
    elif number > 0.5:
        return "danger"
    elif number >= 0:
        return "default"
    

@register.filter('form_couleur')
def form_couleur(res):
    if res == "V":
        return "primary"
    elif res == "N":
        return "default"
    elif res == "D":
        return "danger"

    
@register.filter('start0')
def start0(number):
    try:
        if 0 <= int(number) <= 9 :
            if type(number) is float :
                return round(number, 2)
            return "0"+str(number)
        return number
    except :
        return "00"



@register.filter('dict_value')
def get_value_from_dict(dict_data, key):
    if key:
        try:
            return dict_data[key]
        except :
            try:
                return dict_data[str(key)]
            except :
                return ""
    return ""



@register.filter('rounded')
def rounded(value):
    try:
        return round(value, 2)
    except :
        return value


@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except :
        return value


@register.filter
def to_int(value):
    return int(value)




@register.filter
def sub(value, arg):
    return value - arg



@register.filter("next")
def next(value, arg = 1):
    return value + timedelta(days = arg)


@register.filter("prev")
def next(value, arg = 1):
    return value - timedelta(days = arg)

    

@register.inclusion_tag('djutils/sort_th.html', takes_context=True)
def sort_th(context, sort_param_name, label):
    return {
        'is_current': context['sort_params'][sort_param_name]['is_current'],
        'is_reversed': context['sort_params'][sort_param_name]['is_reversed'],
        'url': context['sort_params'][sort_param_name]['url'],
        'label': label,
    }