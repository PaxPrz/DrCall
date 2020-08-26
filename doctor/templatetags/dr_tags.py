from django import template
import datetime

register = template.Library()

@register.filter(name='listEducation')
def listEducation(value):
    return ' / '.join(x.education for x in value)

@register.filter(name='listSpeciality')
def listSpeciality(value):
    return [(a.speciality, a.description) for a in value]

@register.filter(name='listHospital')
def listHospital(value):
    return [(a.hospital, a.location) for a in value]

@register.filter(name='getAge')
def getAge(value):
    if isinstance(value, datetime.date):
        age = datetime.date.today() - value
        return str(int(age.days/365))
    return "Unknown"

@register.filter(name='getRating')
def getRating(value):
    if len(value)==0:
        return '0'
    rating = 0
    for v in value:
        rating += v.rating
    return '{:.2f}'.format(rating/len(value))