from django import template
from django.utils import timezone
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

@register.filter(name='timeCheck')
def timeCheck(value):
    now = timezone.now()
    if value < now:
        print("expire")
        return "Expired"
    elif value >= now+timezone.timedelta(minutes=5):
        print("FUTURE")
        return "Message"
    else:
        print("its time")
        return "Call"

@register.filter(name='countMed')
def countMed(value):
    count = 0
    for m in value:
        count += len(m.medicine_set.all())
    return str(count)

@register.filter(name='isWithinADay')
def isWithinADay(value):
    if value >= timezone.now()-timezone.timedelta(days=1):
        return True
    return False

@register.filter(name='isWithinHours')
def isWithinHours(value, arg):
    if value >= timezone.now()-timezone.timedelta(hours=int(arg)):
        return True
    return False