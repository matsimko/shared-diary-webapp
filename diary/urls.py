from django.urls import path, include

from . import views

#to differentiate between template names across apps, namescape them:
#app_name = 'diary' #and then in the template: {% url 'diary:urlname' %}
urlpatterns = [
    path('', views.get_diaries, name='diaries'),
    path('new-diary-form', views.new_diary_form, name='diary_form'),
    path('create-diary', views.create_diary, name='create_diary'),
    path('diary/<int:diary_id>/', include([
        path('', views.get_diary, name='diary'),
        path('chapter/<int:day>/<int:month>/<int:year>/', include([
            path('', views.get_diary, name='diary_with_chapter'),
            path('json', views.get_chapter, name='chapter'),
            path('tab/<str:tab>', views.get_diary, name='diary_with_chapter_tab'),
            path('new-story-form', views.new_story_form, name='story_form'),
            path('create-story', views.create_story, name='create_story'),
            path('new-note-form', views.new_note_form, name='note_form'),
            path('create-note', views.create_note, name='create_note'),
            path('new-tasklist-form', views.new_tasklist_form, name='tasklist_form'),
            path('create-tasklist', views.create_tasklist, name='create_tasklist'),
        ]))
    ])),
    path('update-note/<int:note_id>', views.update_note, name='update_note'),
    path('delete-note/<int:note_id>', views.delete_note, name='delete_note'),
    path('update-task-list/<int:tasklist_id>', views.update_tasklist, name='update_tasklist'),

]