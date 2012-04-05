from django.contrib import admin
from portfolio.models import *


class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'year')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')

class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'type')
    
class MediaInline(admin.TabularInline):
    model = Media
    extra = 10

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('service', 'work')
    exclude = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': ('work', 'order', 'service', 'description', 'technology', ('url', 'itunes'), 'active_status'),
        }),
    )
    inlines = [
        MediaInline
    ]

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 5

class WorkAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('created', 'modified')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'order', 'date_launched', 'logo', 'description', 'client', 'review', 'award', 'url', 'style', 'featured_status', 'active_status'),
        }),
    )
    inlines = [
        ProjectInline
    ]


admin.site.register(Award, AwardAdmin)
admin.site.register(Client)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Technology)
admin.site.register(Media, MediaAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Work, WorkAdmin)