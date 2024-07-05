from django.contrib import admin
from .models import User, File, Consideration, Log, Download, Classification
from .forms import FileUploadForm, ConsiderationUploadForm

def approve_considerations(modeladmin, request, queryset):
    queryset.update(is_approved=True)
approve_considerations.short_description = "Approve selected considerations"

class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class FileAdmin(admin.ModelAdmin):
    form = FileUploadForm
    list_display = ('display_name', 'upload_time', 'description', 'classification')
    list_filter = ('upload_time', 'classification')
    search_fields = ('display_name',)
    fields = ('display_name', 'description', 'file', 'classification')

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
admin.site.register(File, FileAdmin)
admin.site.register(Consideration, ConsiderationAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Download)
admin.site.register(Classification, ClassificationAdmin)