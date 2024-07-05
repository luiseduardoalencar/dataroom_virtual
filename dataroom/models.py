from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Classification(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255, default="")
    cnpj = models.CharField(max_length=18, unique=True, default="")
    social_reason = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=255, default="")
    representative_name = models.CharField(max_length=255, default="")
    position = models.CharField(max_length=255, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'company_name', 'cnpj', 'social_reason', 'phone', 'address', 'representative_name', 'position']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='dataroom_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='dataroom_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class File(models.Model):
    filename = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file_data = models.BinaryField(editable=False)
    upload_time = models.DateTimeField(auto_now_add=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name='files', null=True, blank=True)
    
class Consideration(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='considerations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consideration_filename = models.CharField(max_length=255)
    consideration_data = models.BinaryField(null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    download_time = models.DateTimeField(auto_now_add=True)


class Log(models.Model):
    ACTION_CHOICES = [
        ('upload', 'Upload'),
        ('download', 'Download'),
        ('upload_consideration', 'Upload Consideration'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} {self.action} {self.filename} at {self.timestamp}"
