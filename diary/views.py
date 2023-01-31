import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string

from accounts.models import Group
from djangoWebApp.utils import chunks
from .forms import DiaryForm, StoryForm, NoteForm, TaskListForm
from .models import Diary, Chapter, Story, Note, TaskList, Task


# Create your views here.

@login_required
def get_diaries(request):
    # select diaries which belong to one of the groups that the user is in
    groups = request.user.group_set.all()
    diaries = Diary.objects.filter(group__in=groups)  # group__id__in=groups.values_list('id')
    # divide the list into groups of 4
    chunked_diaries = chunks(diaries, 4)
    return render(request, 'diary/diaries.html', {'chunked_diaries': chunked_diaries})


@login_required
def new_diary_form(request):
    diary_form = DiaryForm(user=request.user)

    return render(request, 'diary/diary_form.html', {'diary_form': diary_form})


@login_required
def create_diary(request):
    if request.method == 'POST':
        diary_form = DiaryForm(request.POST, user=request.user)
        if diary_form.is_valid():  # it also validates that the group is one of the groups that user is in
            name = diary_form.cleaned_data['name']
            group = diary_form.cleaned_data['group']
            # create a new group if none was selected
            if group is None:
                group_name = '{}: {}'.format(request.user.username, name)
                group = Group(name=group_name)
                group.save()
                group.users.add(request.user)
            diary = Diary(name=name, group=group)
            diary.save()

    return redirect('diaries')


@login_required
def get_diary(request, diary_id, day=None, month=None, year=None, tab="stories"):
    diary = get_object_or_404(Diary, pk=diary_id)
    if not diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    return render(request, 'diary/diary.html', {'diary': diary, 'day': day,
                                                'month': month, 'year': year,
                                                'tab': tab})


def get_chapter_or_404(diary_id, day, month, year):
    date = datetime.date(year, month, day)
    chapter = get_object_or_404(Chapter, diary__id=diary_id, date=date)
    return chapter


@login_required
def get_chapter(request, diary_id, day, month, year):
    diary = Diary.objects.get(pk=diary_id)
    if not diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    date = datetime.date(year, month, day)
    try:
        chapter = Chapter.objects.get(diary__id=diary_id, date=date)
    except Chapter.DoesNotExist:
        chapter = Chapter(diary=diary, date=date)
        chapter.save()


    # there might be a better solution to this
    parent_url = {'diary_id': diary_id, 'day': day, 'month': month, 'year': year}

    stories_html = render_to_string('diary/stories.html', {'stories': chapter.story_set.all(),
                                                           'url': parent_url, 'user': request.user}, request)
    notes_html = render_to_string('diary/notes.html', {'notes': chapter.note_set.all(),
                                                       'url': parent_url, 'user': request.user}, request)
    tasklists_html = render_to_string('diary/tasklists.html', {'tasklists': chapter.tasklist_set.all(),
                                                               'url': parent_url, 'user': request.user}, request)
    return JsonResponse({'stories': stories_html, 'notes': notes_html, 'tasklists': tasklists_html})


@login_required
def new_story_form(request, diary_id, day, month, year):
    chapter = get_chapter_or_404(diary_id, day, month, year)
    if not chapter.diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    parent_url = {'diary_id': diary_id, 'day': day, 'month': month, 'year': year}
    story_form = StoryForm()
    return render(request, 'diary/story_form.html', {'story_form': story_form, 'url': parent_url})


@login_required
def create_story(request, diary_id, day, month, year):
    chapter = get_chapter_or_404(diary_id, day, month, year)
    if not chapter.diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    if request.method == 'POST':
        story_form = StoryForm(request.POST)
        if story_form.is_valid():
            title = story_form.cleaned_data['title']
            text = story_form.cleaned_data['text']
            story = Story(chapter=chapter, title=title, text=text, author=request.user)
            story.save()

    return redirect('diary_with_chapter_tab', diary_id=diary_id,
                    day=day, month=month, year=year, tab="stories")



@login_required
def new_note_form(request, diary_id, day, month, year):
    chapter = get_chapter_or_404(diary_id, day, month, year)
    if not chapter.diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    parent_url = {'diary_id': diary_id, 'day': day, 'month': month, 'year': year}
    note_form = NoteForm()
    return render(request, 'diary/note_form.html', {'note_form': note_form, 'url': parent_url})


@login_required
def create_note(request, diary_id, day, month, year):
    chapter = get_chapter_or_404(diary_id, day, month, year)
    if not chapter.diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            text = note_form.cleaned_data['text']
            note = Note(chapter=chapter, text=text, author=request.user)
            note.save()

    return redirect('diary_with_chapter_tab', diary_id=diary_id,
                    day=day, month=month, year=year, tab="notes")


@login_required
def update_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    # if not note.chapter.diary.group.users.filter(id=request.user.id).exists():
    if note.author is not None and note.author != request.user:
        return HttpResponse(status=403)

    if request.method == 'POST':
        # is there any disadvantage compared to defining an UpdateForm in this case?
        # I dont't think so (the is_valid() wouldn't really do anything)
        text = request.POST.get('text', '')
        note.text = text
        note.save()

    date = note.chapter.date
    return redirect('diary_with_chapter_tab', diary_id=note.chapter.diary.id,
                    day=date.day, month=date.month, year=date.year, tab="notes")


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    # if not note.chapter.diary.group.users.filter(id=request.user.id).exists():
    if note.author is not None and note.author != request.user:
        return HttpResponse(status=403)

    if request.method == 'POST':
        note.delete()

    date = note.chapter.date
    return redirect('diary_with_chapter_tab', diary_id=note.chapter.diary.id,
                    day=date.day, month=date.month, year=date.year, tab="notes")


@login_required
def new_tasklist_form(request, diary_id, day, month, year):
    chapter = get_chapter_or_404(diary_id, day, month, year)
    if not chapter.diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    parent_url = {'diary_id': diary_id, 'day': day, 'month': month, 'year': year}
    tasklist_form = TaskListForm()
    return render(request, 'diary/tasklist_form.html', {'tasklist_form': tasklist_form, 'url': parent_url})


@login_required
def create_tasklist(request, diary_id, day, month, year):
    chapter = get_chapter_or_404(diary_id, day, month, year)
    if not chapter.diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    if request.method == 'POST':
        tasklist_form = TaskListForm(request.POST)
        if tasklist_form.is_valid():
            name = tasklist_form.cleaned_data['name']
            tasklist = TaskList(chapter=chapter, name=name, author=request.user)
            tasklist.save()

    return redirect('diary_with_chapter_tab', diary_id=diary_id,
                    day=day, month=month, year=year, tab="tasklists")



@login_required
@transaction.atomic
def update_tasklist(request, tasklist_id):
    tasklist = get_object_or_404(TaskList, pk=tasklist_id)
    # if tasklist.author is not None and tasklist.author != request.user:
    if not tasklist.chapter.diary.group.users.filter(id=request.user.id).exists():
        return HttpResponse(status=403)

    if request.method == 'POST':
        tasks_data = json.loads(request.body)
        # replace all tasks with the sent list
        tasklist.task_set.all().delete()
        for task in tasks_data:
            task = Task(text=task['text'], is_finished=task['is_finished'],
                              task_list=tasklist, author=request.user)
            task.save()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
