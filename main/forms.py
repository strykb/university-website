from django import forms
from .models import Department,Course, Module, Group, Exam, Grade 
from accounts.models import Account

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ['slug']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['slug', 'department']

class GroupForm(forms.ModelForm):  
    class Meta:
        model = Group
        fields = ['name','students']
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set initial queryset of students field to none
        self.fields['students'].queryset = Account.objects.none()

        if 'students' in self.data:
            # when form is submitted and has students in it
            # set queryset of students field to all students
            students = Account.objects.filter(is_student=True)
            self.fields['students'].queryset = students

        elif self.instance.pk:
            # when group is edited set queryset of students field
            # to previously saved students
            self.fields['students'].queryset = self.instance.students

class ModuleForm(forms.ModelForm):
    tutors = forms.ModelMultipleChoiceField(
        queryset=Account.objects.filter(is_tutor=True))

    class Meta:
        model = Module
        exclude = ['course']

class ExamForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Exam
        exclude = ['module', 'tutor']

    def __init__(self, *args, **kwargs):
        if 'module' in kwargs:
            # module is passed to kwargs when exam is created
            module = kwargs.pop('module')
        super(ExamForm, self).__init__(*args, **kwargs)
        # sets group field queryset
        # to groups linked to currently selected course
        if self.instance.pk:
            # if exam exists (is edited)
            self.fields['group'].queryset = self.instance.module.course.groups
        else:
            # if exam is being created
            self.fields['group'].queryset = module.course.groups

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        exclude = ['exam']

    def __init__(self, *args, **kwargs):
        exam = kwargs.pop('exam')
        super().__init__(*args, **kwargs)
        # sets student field queryset
        # to students linked to currently selected exam
        self.fields['student'].queryset = exam.group.students