from django.contrib import admin
from .models import User, Group, Membership, Invite

# Register your models here.
admin.site.register(Group)
admin.site.register(User)
admin.site.register(Membership)
admin.site.register(Invite)