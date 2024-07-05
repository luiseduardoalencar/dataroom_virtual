from django.contrib import admin
from .models import User, File, Consideration, Log, Download
from .forms import FileUploadForm, ConsiderationUploadForm

def approve_considerations(modeladmin, request, queryset):
    queryset.update(is_approved=True)
approve_considerations.short_description = "Approve selected considerations"


class FileAdmin(admin.ModelAdmin):
    form = FileUploadForm
    list_display = ('display_name', 'upload_time', 'description')
    list_filter = ('upload_time',)
    search_fields = ('display_name',)
    fields = ('display_name', 'description', 'file')

class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'filename', 'timestamp')
    list_filter = ('action', 'timestamp')

class ConsiderationAdmin(admin.ModelAdmin):
    form = ConsiderationUploadForm
    list_display = ('file', 'user', 'consideration_filename', 'upload_time', 'is_approved')
    list_filter = ('is_approved', 'upload_time')
    search_fields = ('consideration_filename',)
    fields = ('consideration_file', 'file', 'user', 'is_approved')
    actions = [approve_considerations]


admin.site.register(User)
admin.site.register(File, FileAdmin)  # Use FileAdmin here
admin.site.register(Consideration, ConsiderationAdmin)  # Use ConsiderationAdmin here
admin.site.register(Log, LogAdmin)
admin.site.register(Download)
