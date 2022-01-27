from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect
from django.core.management import call_command
from django.urls import reverse, reverse_lazy
from .models import Department, Course, Group, Module, Exam, Grade
from .forms import (GroupForm, DepartmentForm, CourseForm,
                    ExamForm, GradeForm, ModuleForm)
from accounts.models import Account

def restore_db(request):
    # for demonstration purposes
    # restores the database
    call_command('loaddata', 'backup.json')
    return redirect('index')

class IndexView(TemplateView):
    template_name = 'main/index.html'

class DepartmentListView(ListView):
    model = Department
    template_name = 'main/departments.html'
    context_object_name = 'departments'

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'main/department.html'
    
class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'main/create_department.html'
    success_url = reverse_lazy('departments')
    
class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'main/edit_department.html'

    def get_success_url(self):
        return reverse('department', kwargs={'slug': self.kwargs['slug']})
    
class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'main/delete_department.html'
    success_url = reverse_lazy('departments')

class CourseDetailView(DetailView):
    model = Course
    template_name = 'main/course.html'

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'main/create_course.html'

    def form_valid(self, form):
        # sets department field value to currently viewed department
        department_id = Department.objects.get(
                        slug=self.kwargs.get('slug')
                        ).pk
        form.instance.department_id = department_id
        return super(CourseCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('department', kwargs={'slug': self.kwargs['slug']})

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'main/edit_course.html'
    
    def get_success_url(self):
        return reverse('course', kwargs={'slug': self.kwargs['slug']})

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    form_class = CourseForm
    template_name = 'main/delete_course.html'

    def get_success_url(self):
        # redirects to department linked to deleted course
        slug = Course.objects.get(slug=self.kwargs['slug']).department.slug
        return reverse('department', kwargs={'slug': slug})

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'main/group.html'

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'main/create_group.html'
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            # filters students based on term searched in form field
            term = request.GET.get('term')
            students = Account.objects.filter(
                (Q(first_name__contains=term)
                | Q(last_name__contains=term)
                | Q(id__contains=term))
                & Q(is_student=True))
            response_content = list(students.values())
            return JsonResponse(response_content, safe=False)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('course', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        # sets course field value to currently viewed course
        course_id = Course.objects.get(slug=self.kwargs.get('slug')).pk
        form.instance.course_id = course_id
        return super(GroupCreateView, self).form_valid(form)

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'main/edit_group.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            # filters students based on term searched in form field
            term = request.GET.get('term')
            students = Account.objects.filter(
                (Q(first_name__contains=term)
                | Q(last_name__contains=term)
                | Q(id__contains=term))
                & Q(is_student=True))
            response_content = list(students.values())
            return JsonResponse(response_content, safe=False)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('group', kwargs={'pk': self.kwargs['pk']})

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'main/delete_group.html'

    def get_success_url(self):
        # redirects to course linked to deleted group
        slug = Group.objects.get(pk=self.kwargs['pk']).course.slug
        return reverse('course', kwargs={'slug': slug})

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = 'main/module.html'

class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'main/edit_module.html'
    
    def get_success_url(self):
        return reverse('module', kwargs={'pk': self.kwargs['pk']})

class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'main/create_module.html'

    def get_success_url(self):
        return reverse('course', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form):
        # sets course field value to currently viewed course
        course_id = Course.objects.get(slug=self.kwargs.get('slug')).pk
        form.instance.course_id = course_id
        return super(ModuleCreateView, self).form_valid(form)

class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Module
    template_name = 'main/delete_module.html'
    success_url = reverse_lazy('modules')

class ExamCreateView(LoginRequiredMixin, CreateView):
    form_class = ExamForm
    template_name = 'main/create_exam.html'

    def get_success_url(self):
        return reverse('module', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self, *args, **kwargs):
        # passes module to form
        kwargs = super(ExamCreateView, self).get_form_kwargs()
        kwargs['module'] = Module.objects.get(pk=self.kwargs.get('pk'))
        return kwargs

    def form_valid(self, form):
        # sets values of module and tutor fields
        module_id = Module.objects.get(id=self.kwargs.get('pk')).pk
        tutor = self.request.user.id
        form.instance.module_id = module_id
        form.instance.tutor_id = tutor
        return super(ExamCreateView, self).form_valid(form)

class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'main/exam.html'

class ExamUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'main/edit_exam.html'
    
    def get_success_url(self):
        return reverse('exam', kwargs={'pk': self.kwargs['pk']})

class ExamDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = 'main/delete_exam.html'

    def get_success_url(self):
        # redirects to module linked to deleted exam
        return reverse('module', kwargs={'pk': self.object.module.id})

class GradeCreateView(LoginRequiredMixin, CreateView):
    form_class = GradeForm
    template_name = 'main/create_grade.html'

    def get_context_data(self, **kwargs):
        # passes exam to template
        context = super(GradeCreateView, self).get_context_data(**kwargs)
        context['exam'] = Exam.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_success_url(self):
        return reverse('exam', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self, *args, **kwargs):
        # passes exam to form
        kwargs = super(GradeCreateView, self).get_form_kwargs()
        kwargs['exam'] = Exam.objects.get(pk=self.kwargs.get('pk'))
        return kwargs

    def form_valid(self, form):
        # sets value of exam field
        exam_id = Exam.objects.get(id=self.kwargs.get('pk')).pk
        form.instance.exam_id = exam_id
        return super(GradeCreateView, self).form_valid(form)

class GradeUpdateView(LoginRequiredMixin, UpdateView):
    model = Grade
    template_name = 'main/edit_grade.html'
    fields = ['value']

    def get_success_url(self):
        return reverse('exam', kwargs={'pk': self.object.exam.id})

class GradeDeleteView(LoginRequiredMixin, DeleteView):
    model = Grade
    template_name = 'main/delete_grade.html'

    def get_success_url(self):
        # redirects to exam linked to deleted grade
        return reverse('exam', kwargs={'pk': self.object.exam.id})
