from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Account

UserModel = get_user_model()
class CreateAccountForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name','password1','password2']

class ApproveStudentForm(forms.ModelForm):
    # approve pending user as student
    class Meta:
        model = Account
        fields = []

    def save(self, commit=True):
        model = super(ApproveStudentForm, self).save(commit=False)
        model.is_student = True
        if commit:
            model.save()
        return model