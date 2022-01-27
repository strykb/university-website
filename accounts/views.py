from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import ApproveStudentForm, CreateAccountForm
from .models import Account

class RegisterView(CreateView):
    form_class = CreateAccountForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UsersListMixin(object):
    # mixin for listviews with users
    queryset = Account.objects.none()
    template_name = 'accounts/users_list.html'
    context_object_name = 'members'
    paginate_by = 15

    def get_queryset(self):
        # query users using search bar
        result = super().get_queryset()
        search = self.request.GET.get('search') # searched term

        # filters users based on view's user_type attribute
        if self.users_type == 'students':
            users = Account.objects.filter(is_student=True)
        elif self.users_type == 'tutors':
            users = Account.objects.filter(is_tutor=True)
        elif self.users_type == 'technicians':
            users = Account.objects.filter(is_technician=True)
        elif self.users_type == 'pending':
            users = Account.objects.filter(
                is_tutor=False, is_technician=False,
                is_student=False, is_superuser=False
                )

        if search:
            # filters users based on searched term
            result = users.filter(
                Q(first_name__contains=search)
                | Q(last_name__contains=search)
                | Q(id__contains=search)
                )
        else:
            # if nothing was searched
            result = users
        return result.order_by('id')

class TutorsListView(LoginRequiredMixin, UsersListMixin, ListView):
    users_type = 'tutors'

class StudentsListView(LoginRequiredMixin, UsersListMixin, ListView):
    users_type = 'students'

class TechniciansListView(LoginRequiredMixin, UsersListMixin, ListView):
    users_type = 'technicians'

class PendingUsersListView(LoginRequiredMixin, UsersListMixin, ListView):
    users_type = 'pending'

class ApproveStudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class=ApproveStudentForm
    template_name = 'accounts/approve_student.html'
    success_url = reverse_lazy('pending_users')

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    # context_object_name = 'member'
    template_name = 'accounts/edit_user.html'
    fields = ['is_tutor', 'is_student', 'is_technician']
    success_url = '/'