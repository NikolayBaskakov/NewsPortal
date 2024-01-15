from django.contrib import admin
from .models import *
# Register your models here.
def update_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'date', 'title', 'rating')
    list_filter = ('date',)
    search_fields = ('name', 'category__name')
    actions = [update_rating]
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)