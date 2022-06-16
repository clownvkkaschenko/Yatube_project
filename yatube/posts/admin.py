from django.contrib import admin
from posts.models import Post, Group, Comment


class CommentAdmin(admin.ModelAdmin):
    """Comment management via admin."""
    list_display = (
        'post',
        'author',
        'text',
        'created'
    )
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class PostAdmin(admin.ModelAdmin):
    """Post management via admin."""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
        'image'
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    """Group management via admin."""
    list_display = (
        'title',
        'slug',
        'description'
    )
    search_fields = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
