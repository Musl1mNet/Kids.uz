from django.contrib import admin

from .forms import PostForm
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent', 'name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['id', 'category', 'title', 'date']
    list_filter = ['category', ]
    autocomplete_fields = ["owner", ]
