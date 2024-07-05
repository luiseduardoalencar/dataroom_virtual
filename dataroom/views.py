from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, FileUploadForm, ConsiderationUploadForm
from .models import File, Log, Consideration
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'dataroom/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'dataroom/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def index(request):
    files = File.objects.all()
    return render(request, 'dataroom/index.html', {'files': files})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()
            Log.objects.create(user=request.user, action='upload', filename=file_instance.filename)
            messages.success(request, 'File uploaded successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Error uploading file. Please ensure the file type is allowed.')
    else:
        form = FileUploadForm()
    return render(request, 'dataroom/upload_file.html', {'form': form})

import logging

logger = logging.getLogger(__name__)

@login_required
def file_detail(request, pk):
    file = get_object_or_404(File, pk=pk)
    considerations = file.considerations.all()
    if request.method == 'POST':
        form = ConsiderationUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                consideration_instance = form.save(commit=False)
                consideration_instance.file = file
                consideration_instance.user = request.user
                consideration_instance.is_approved = False  # Define como não aprovado por padrão
                consideration_instance.save()
                Log.objects.create(user=request.user, action='upload_consideration', filename=consideration_instance.consideration_filename)
                messages.success(request, 'Consideration uploaded successfully. Awaiting approval.')
                return HttpResponseRedirect(request.path_info)
            except Exception as e:
                logger.error(f'Error saving consideration: {e}')
                messages.error(request, f'Error saving consideration: {e}')
        else:
            logger.error(f'Form is not valid: {form.errors}')
            messages.error(request, f'Form is not valid: {form.errors}')
    else:
        form = ConsiderationUploadForm()
    return render(request, 'dataroom/file_detail.html', {'file': file, 'considerations': considerations, 'form': form})

@login_required
def download_file(request, pk):
    file = get_object_or_404(File, pk=pk)
    response = HttpResponse(file.file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
    Log.objects.create(user=request.user, action='download', filename=file.filename)
    return response

@login_required
def download_consideration(request, pk):
    consideration = get_object_or_404(Consideration, pk=pk)
    response = HttpResponse(consideration.consideration_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{consideration.consideration_filename}"'
    return response