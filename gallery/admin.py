from django.contrib import admin
from django.utils.html import format_html
from .models import Store, StoreSection, Photo


class StoreSectionInline(admin.TabularInline):
    model = StoreSection
    extra = 0


class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ("section", "thumbnail_preview", "description", "created_at")
    readonly_fields = ("thumbnail_preview", "created_at")
    extra = 0

    def thumbnail_preview(self, obj):
        if obj and obj.thumbnail:
            return format_html('<img src="{}" style="height:70px;">', obj.thumbnail.url)
        return ""
    thumbnail_preview.short_description = "Preview"


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "city", "state", "photo_count")
    search_fields = ("code", "name", "city", "state")
    list_filter = ("state", "city")
    inlines = [StoreSectionInline, PhotoInline]
    def has_delete_permission(self, request, obj=None):
        # Restrict store delete to superuser when photos exist
        if obj and obj.photos.exists() and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def photo_count(self, obj):
        return obj.photos.count()


@admin.register(StoreSection)
class StoreSectionAdmin(admin.ModelAdmin):
    list_display = ("store", "name", "is_active")
    list_filter = ("store", "is_active")
    search_fields = ("store__code", "name")


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("store", "section", "thumbnail_list", "uploaded_by", "created_at")
    list_filter = ("store", "section", "uploaded_by")
    search_fields = ("store__code", "store__name", "section__name", "description")
    readonly_fields = ("thumbnail_list",)

    def thumbnail_list(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="height:70px;">', obj.thumbnail.url)
        return ""
    thumbnail_list.short_description = "Preview"

# Register your models here.
