from django.contrib import admin
from .models import User, File, Consideration, Log, Download, Classification
from .forms import FileUploadForm, ConsiderationUploadForm, AdminUserCreationForm

def approve_considerations(modeladmin, request, queryset):
    queryset.update(is_approved=True)
approve_considerations.short_description = "Approve selected considerations"

def make_admin(modeladmin, request, queryset):
    queryset.update(is_admin=True)
make_admin.short_description = "Mark selected users as admin"

def make_moderator(modeladmin, request, queryset):
    queryset.update(is_moderator=True)
make_moderator.short_description = "Mark selected users as moderator"

def approve_users(modeladmin, request, queryset):
    queryset.update(is_approved=True)
approve_users.short_description = "Approve selected users"

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

class UserAdmin(admin.ModelAdmin):
    form = AdminUserCreationForm
    list_display = ('email', 'is_admin', 'is_moderator', 'is_approved', 'company_name', 'cnpj')
    list_filter = ('is_admin', 'is_moderator', 'is_approved')
    search_fields = ('email', 'company_name', 'cnpj')
    ordering = ('email',)
    fields = ('email', 'is_admin', 'is_moderator', 'is_approved', 'company_name', 'cnpj', 'social_reason', 'phone', 'address', 'representative_name', 'position')
    readonly_fields = ('last_login', 'date_joined')
    actions = [make_admin, make_moderator, approve_users]

admin.site.register(User, UserAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Consideration, ConsiderationAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(Download)
admin.site.register(Classification, ClassificationAdmin)
