from django import template
from ..models import Department

register = template.Library()

@register.inclusion_tag('main/templatetags/navbar_items.html')
def navbar_items():
    # adds departments dropdown to navbar
    context = {
        'departments': Department.objects.all(),
        }
    return context

@register.inclusion_tag('main/templatetags/departments_preview.html', takes_context=True)
def departments_preview(context):
    # displays departments on home page
    return {
        'departments': Department.objects.all(),
        'user': context['user']
        }

@register.inclusion_tag('main/templatetags/modules_list.html', takes_context=True)
def modules_list(context):
    # displays modules list with active/disabled links for students
    # if student belongs to course -> dispaly active links
    # else -> display disabled links
    course_groups = context['course'].groups.all()
    student_groups = context['user'].groups.all()
    on_course = False
    for group in student_groups:
        if group in course_groups:
            # if student belongs to course
            on_course = True
            break
    return {
        'on_course': on_course,
        'modules': context['course'].modules.all()
    }

@register.inclusion_tag('main/templatetags/grades.html', takes_context=True)
def grades(context):
    # displays grades separated with border
    student_grades = context['student'].grades.all()
    exam = context['exam']
    grades = [g for g in student_grades if g.exam == exam]
    return {'grades':grades}

def on_module(user, module):
    # checks if student attends module
    for group in user.groups.all():
        if group in module.course.groups.all():
            return True
    return False
    
register.filter('on_module', on_module)