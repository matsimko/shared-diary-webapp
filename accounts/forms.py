from django.contrib.auth.forms import UserCreationForm, UserChangeForm as OrigUserChangeForm, AuthenticationForm
from django import forms
from django.db.models import QuerySet, Q, Exists

from .models import User, Invite, Group
from djangoWebApp.forms import StyledForm, StyledModelForm


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class RegisterForm(UserCreationForm): #needed to define this because I use a custom user (and I also added the email field)

    class Meta:
        model = User
        fields = ('username', 'email', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserChangeForm(OrigUserChangeForm):

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class InviteForm(StyledForm):
    #probably no other way but to do it manually like this...
    group_name = forms.CharField(disabled=True, required=False) #disabled fields are not sent, but they are required by default in django...
    group_id = forms.IntegerField(widget=forms.HiddenInput)
    to_user = forms.ModelChoiceField(queryset=User.objects.all()) #use all() and do the validation in the view instead...

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if group is not None and user is not None:
            # exclude users already in the group or invited, later on there might some friendlist to choose from instead of all users
            self.fields['to_user'].queryset = User.objects.all().exclude(
                Q(id__in=group.users.all()) |
                Q(id__in=Invite.objects.filter(group__id=group.id).values_list('to_user__id'))) #using IN instead of EXISTS, cuz I don't if it is possible to do a correlated subquery (i.e., to use the 'user' inside the subquery), but the foreign key cannot be NULL so there is not issue with that
            self.fields['group_name'].initial = group.name
            self.fields['group_id'].initial = group.id

class GroupForm(StyledModelForm):

    class Meta:
        model = Group
        fields = ('name',)



