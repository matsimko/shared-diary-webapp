from django.db import models
from accounts.models import Group, User


# Create your models here.




class Diary(models.Model):
    """Zero or more diaries per group"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE) #each User might have a group, which only he belongs to (this way there is no need for some inheritance, where the would be smth like "Owner", from which would User and Group inherit.
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    """Zero or one chapter in a diary per day"""
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    date = models.DateField('date that the chapter belongs to')
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.diary.name, self.date)

class Story(models.Model):
    """Zero or more stories per chapter"""
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} ({}): {}".format(self.chapter.diary.name, self.chapter.date, self.title)

# class Note(models.Model):
#     """One note per chapter (can be used as a task list for that day)"""
#     chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return "{} ({}): {}".format(self.chapter.diary.name, self.chapter.date, self.title)

class Note(models.Model):
    """Zero or more notes per Chapter"""
    #note = models.ForeignKey(Note, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} ({})".format(self.chapter.diary.name, self.chapter.date)

class TaskList(models.Model):
    """Zero or more task lists per Chapter"""
    #note = models.ForeignKey(Note, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} ({}): {}".format(self.chapter.diary.name, self.chapter.date, self.name)

class Task(models.Model):
    """Zero or more tasks per TaskList"""
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    text = models.CharField(max_length=500)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} ({}): {}".format(self.task_list.chapter.diary.name, self.task_list.chapter.date, self.task_list.name)


