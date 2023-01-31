from django.contrib import admin

from .models import Diary, Note, Task, TaskList, Story, Chapter

# Register your models here.
admin.site.register(Diary)
admin.site.register(Note)
admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(Story)
admin.site.register(Chapter)
