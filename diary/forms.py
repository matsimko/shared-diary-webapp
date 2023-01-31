from django import forms

from accounts.models import Group
from djangoWebApp.forms import  StyledModelForm

from diary.models import Diary, Story, Note, TaskList


class DiaryForm(StyledModelForm):
    # fields can be changed like this, so forms.ModelForm can still be used instead of forms.Form
    group = forms.ModelChoiceField(required=False, queryset=Group.objects.none(), help_text='Leave it empty to automatically create a new group with you in it.')

    class Meta:
        model = Diary
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = user.group_set.all() #if using permissions, then use Membership.objects

class StoryForm(StyledModelForm):

    class Meta:
        model = Story
        fields = ('title', 'text')

class NoteForm(StyledModelForm):

    class Meta:
        model = Note
        fields = ('text',)

class TaskListForm(StyledModelForm):
    class Meta:
        model = TaskList
        fields = ('name',)
