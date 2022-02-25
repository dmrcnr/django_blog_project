from django.contrib import admin

from .models import Article,Comment

# Register your models here.

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","author","created_date"]
    list_display_links =["title","author","created_date"]
    search_fields = ["title"]
    list_filter = ["created_date"]
    class Meta:
        model=Article

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["comment_content","comment_author"]
    search_fields = ["comment_author"]
    list_filter = ["comment_date"]
    class Meta:
        model = Comment

