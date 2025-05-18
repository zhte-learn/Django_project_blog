from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "slug",
    )
    search_fields = ("title",)
    list_filter = ("title",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pub_date",
        "author",
        "location",
        "category",
    )
    search_fields = ("title",)
    list_filter = ("category", "author",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "author",
        "created_at",
    )
    search_fields = ("author__username", "text")
    list_filter = ("post", "author")


admin.site.empty_value_display = 'Не задано'
