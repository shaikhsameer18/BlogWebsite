from django.contrib import admin
from .models import Category, Post


# For configuration of Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'description', 'url', 'add_date')
    search_fields = ('title',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('cat',)
    list_per_page = 50

    class Media:
        js = ('https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js', 'js/script.js',)


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
