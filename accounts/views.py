from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as OrigLoginView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterForm, InviteForm, GroupForm, LoginForm
from .models import Group, Invite, User, Membership



#class-based view
class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('custom_login') #reverse gets the url under the name 'custom_login' (lazily, because, for generic views, the urls are not loaded, when the file is imported
    template_name = 'registration/signup.html' #the RegisterForm will be passed as context to this template


#for styling-sake (other solution would be to not use form.as_p, but instead access the individual attributes: {{ form.username }}..
class LoginView(OrigLoginView):
    authentication_form = LoginForm
    template_name = 'registration/login.html'


#the class-based view isn't really that simpler than a function in this case...
class GroupListView(LoginRequiredMixin, generic.list.ListView): #I could also use a DetailView for the user in this case
    template_name = 'groups/groups.html'

    def get_queryset(self): #the default object_list / group_list
        return self.request.user.group_set.all()


@login_required #basically checks for: request.user.is_authenticated() and if false, then redirects
def invites(request):
    return render(request, 'groups/invites.html', {'user': request.user})


# <form method="POST" action="{% url  'cancel_invite' %}">
# {% csrf_token %}
# <input type="text" name="invite_id" hidden value="{{ inv.id }}"/>
# <input type="submit" value="Cancel"/>
# </form>

#Using such POST request prevents the user to cancel an invite from an url,
# but he can still send a POST request by making the form element, or adjusting the invite_id
#of an existing cancel_invite form, so, it will need to be checked server-side.
#Also, the following code is probably liable to SQL injection...

# @login_required
# def cancel_invite(request):
#     if request.method == 'POST':
#         invite_id = int(request.POST.get('invite_id', 0))
#         invite = get_object_or_404(Invite, pk=invite_id)
#         invite.delete()
#     return redirect('invites')

@login_required
def cancel_invite(request, invite_id):
    invite = get_object_or_404(Invite, pk=invite_id)
    if invite.from_user != request.user:
        return HttpResponse(status=403) #forbidden
    invite.delete()
    return redirect('invites')

@login_required
def invite(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    invite_form = InviteForm(group=group, user=request.user)
    return render(request, 'groups/invite.html', {'invite_form' : invite_form})

@login_required
def send_invite(request):
    if request.method == 'POST':
        invite_form = InviteForm(request.POST)
        if invite_form.is_valid():
            from_user = request.user
            to_user = invite_form.cleaned_data['to_user']
            group_id = invite_form.cleaned_data['group_id']
            group = Group.objects.get(pk=group_id)
            if (not group.users.filter(pk=from_user.id).exists()
                    or group.users.filter(pk=to_user.id).exists()):
                    #or Invite.objects.filter(group__id=group_id, to_user__id=to_user.id).exists()): #this is handled by the unique_together in the Invite model
                # the from_user is not in the group, so he cannot invite
                # or the to_user is already in the group
                # or the to_user has been already invited
                # (later on there might also be roles within the group which can restrict if he can invite or not)
                return HttpResponse(status=403)
            invite = Invite(from_user=from_user, to_user=to_user, group=group)
            invite.save()

    field_errors = [(field.label, field.errors) for field in invite_form]
    print(field_errors)
    return redirect('invites')


@login_required()
def leave_group(request, group_id):
    #membership = get_object_or_404(Membership, group_id=group_id, user_id=request.user.id)
    #membership.delete()
    group = get_object_or_404(Group, pk=group_id)
    user = group.users.remove(request.user)
    # if he was the last member, delete the group
    if not group.users.exists():
        group.delete()
    return redirect('groups')

def handle_invite(request, invite_id, accepted):
    invite = get_object_or_404(Invite, pk=invite_id)
    if invite.to_user != request.user:
        return HttpResponse(status=403)  # forbidden

    if accepted:
        membership = Membership(group=invite.group, user=invite.to_user)
        membership.save()
    invite.delete()
    return redirect('invites')

@login_required
@transaction.atomic #this prevents not creating membership but deleting the invite,
                    #or creating the membership and not deleting the invite,
                    #but idk if those situations can ever happen TODO: ???
def accept_invite(request, invite_id):
    return handle_invite(request, invite_id, True)

@login_required
def decline_invite(request, invite_id):
    return handle_invite(request, invite_id, False)

@login_required
def get_group_form(request):
    group_form = GroupForm()
    return render(request, 'groups/group_form.html', context={'group_form': group_form})

@login_required
def create_group(request):
    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            name = group_form.cleaned_data['name']
            group = Group(name=name)
            group.save()
            group.users.add(request.user)

    return redirect('groups')

