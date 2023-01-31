from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # v settings.py: AUTH_USER_MODEL = 'accounts.User'

    pass

# ??? "Group" from contrib.auth will be used for permissions, and it doesn't make much sense to use it for general groups for diaries etc.
class Group(models.Model):
    name = models.CharField(max_length=100)
    # possibly add an "intersection-entity" "Member" using "through" kw arg,
    # in case additional info for each member of the group is needed
    #for example, date of joining, and some role which will imply his permissions
    users = models.ManyToManyField(User, through='Membership') #this line is only useful for convenience during querying
    creation_date = models.DateTimeField(auto_now_add=True)

    def users_str(self):
        return ', '.join([u.username for u in self.users.all()])

    def __str__(self):
        return self.name


class Membership(models.Model):
    """Represents the membership of one user in one group""" #useful for the possibility of permissions of users within groups and easily defined cascade delete
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    creation_date = models.DateTimeField('date joined', auto_now_add=True)
    #possibly add 'role', which will imply the user's permissions within the group

    def __str__(self):
        return "Group: {}, User: {}".format(self.group, self.user)


class Invite(models.Model):
    """A user might have zero or one active invites to each group"""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites_from') #or make the attribute nullable and make it SET_NULL?
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invites_to') #related name is required to differentiate between the two when querying from the model User (can be used also to change the default classname_set to smth else)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    creation_date = models.DateTimeField('date of invite', auto_now_add=True)

    class Meta:
        unique_together = ('to_user', 'group',) #this way I dont need to manually check for duplicate invites

    def __str__(self):
        return "Group: {}, From: {}, To: {}".format(self.group, self.from_user, self.to_user)