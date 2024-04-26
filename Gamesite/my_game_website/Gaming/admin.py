from django.contrib import admin

from .models import Comment, Profilis, Game

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploader', 'date')
    list_filter = ('title', 'uploader', 'date')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('game', 'commenter', 'content', 'date_created')

admin.site.register(Profilis)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Game, GameAdmin)
