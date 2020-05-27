from django.contrib import admin
# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from .models import *

class FilmAdmin(admin.ModelAdmin):
    fields = [("film_title", "year", "genre", "summary")]

class CommentAdmin(admin.ModelAdmin):
    fields = ["film_comment", "user", "content", "timestamp"]

class PhotoAdmin(admin.ModelAdmin):
    fields = ["photo_film", "image"]

admin.site.register(Film)
admin.site.register(Comment)
admin.site.register(Photo)
