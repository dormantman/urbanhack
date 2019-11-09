from django.contrib import admin
from problems.models import Tag, Mistake, Problem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Mistake)
class MistakeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'mistake', 'solved']
