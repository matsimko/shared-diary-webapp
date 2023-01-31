from django.urls import path

from . import views

urlpatterns = [
    path('sign-up', views.SignUpView.as_view(), name='signup'),
    path('log-in', views.LoginView.as_view(), name='custom_login'), #url 'login' is used by django.auth and I dont know how to get rid of it, so I am using 'log-in' instead
    path('groups', views.GroupListView.as_view(), name='groups'),
    path('invites', views.invites, name='invites'),
    path('cancel-invite/<int:invite_id>', views.cancel_invite, name='cancel_invite'),
    path('invite/<int:group_id>', views.invite, name='invite'),
    path('send-invite', views.send_invite, name='send_invite'),
    path('leave-group/<int:group_id>', views.leave_group, name='leave_group'),
    path('accept-invite/<int:invite_id>', views.accept_invite, name='accept_invite'),
    path('decline-invite/<int:invite_id>', views.decline_invite, name='decline_invite'),
    path('create-group-form', views.get_group_form, name='get_group_form'),
    path('create-group', views.create_group, name='create_group'),
]