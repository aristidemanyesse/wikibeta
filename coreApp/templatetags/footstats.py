# coding: utf-8
import json
from django import template
import sqlparse
from fractions import Fraction

register = template.Library()


@register.filter('home')
def home(matchs):
    total = 0
    for item in matchs:
        result =  item.get_result()
        total += 1 if result.home_score > result.away_score else 0
    return total


@register.filter('away')
def away(matchs):
    total = 0
    for item in matchs:
        result =  item.get_result()
        total += 1 if result.home_score < result.away_score else 0
    return total


@register.filter('draw')
def draw(matchs):
    total = 0
    for item in matchs:
        result =  item.get_result()
        total += 1 if result.home_score == result.away_score else 0
    return total



@register.filter('plus_but')
def plus_but(matchs, nb):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_score + result.away_score > nb:
            total += 1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('moins_but')
def moins_but(matchs, nb):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_score + result.away_score < nb:
            total += 1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('plus_but_first_half')
def plus_but_first_half(matchs, nb):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None :
            if result.home_half_score + result.away_half_score > nb:
                total += 1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('moins_but_first_half')
def moins_but_first_half(matchs, nb):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None :
            if result.home_half_score + result.away_half_score < nb:
                total += 1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('plus_but_second_half')
def plus_but_first_half(matchs, nb):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None :
            if result.home_score - result.home_half_score + result.away_score - result.away_half_score > nb:
                total += 1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('moins_but_second_half')
def moins_but_first_half(matchs, nb):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None :
            if result.home_score - result.home_half_score + result.away_score - result.away_half_score < nb:
                total += 1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None



@register.filter('cs')
def cs(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_score == 0 or  result.away_score == 0:
            total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None

@register.filter('first_half_cs')
def first_half_cs(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None:
            if result.home_half_score == 0 or result.away_half_score == 0:
                total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('second_half_cs')
def second_half_cs(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None:
            if result.home_score - result.home_half_score == 0 or result.away_score - result.away_half_score == 0:
                total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('btts')
def btts(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_score > 0 and result.away_score > 0:
            total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('first_half_btts')
def first_half_btts(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None:
            if result.home_half_score > 0 and  result.away_half_score > 0:
                total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('second_half_btts')
def second_half_btts(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None:
            if result.home_score - result.home_half_score > 0 and  result.away_score -result.away_half_score > 0:
                total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None


@register.filter('_12')
def _12(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_score !=  result.away_score:
            total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None
    
    

@register.filter('first_half_12')
def first_half_12(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None :
            if result.home_half_score !=  result.away_half_score:
                total +=1
    return total
    # return round(total* 100/len(matchs),2) if len(matchs) > 0 else None
    
    
@register.filter('second_half_12')
def second_half_12(matchs):
    total = 0
    for match in matchs:
        result = match.get_result()
        if result.home_half_score is not None :
            if result.home_score - result.home_half_score !=  result.away_score - result.away_half_score:
                total +=1
    return round(total* 100/len(matchs),2) if len(matchs) > 0 else None