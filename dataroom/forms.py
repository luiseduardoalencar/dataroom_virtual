from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import File, Consideration, User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    representative_name = forms.CharField(max_length=255, required=True)
    position = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = [
            'company_name', 'cnpj', 'social_reason', 'phone', 'email', 'address',
            'representative_name', 'position', 'password1', 'password2'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000000000000'}),
            'social_reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Social reason'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 0000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'representative_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representative name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        cnpj = ''.join(filter(str.isdigit, cnpj))
        if User.objects.filter(cnpj=cnpj).exists():
            raise ValidationError('CNPJ já cadastrado')
        return cnpj

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        user.representative_name = self.cleaned_data['representative_name']
        user.position = self.cleaned_data['position']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class FileUploadForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = File
        fields = ['file', 'display_name', 'description']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        file_instance = super().save(commit=False)
        uploaded_file = self.cleaned_data.get('file')
        file_instance.filename = uploaded_file.name
        file_instance.file_data = uploaded_file.read()
        if commit:
            file_instance.save()
        return file_instance

class ConsiderationUploadForm(forms.ModelForm):
    consideration_file = forms.FileField()

    class Meta:
        model = Consideration
        fields = ['consideration_file']

    def save(self, commit=True):
        consideration_instance = super().save(commit=False)
        uploaded_file = self.cleaned_data.get('consideration_file')
        if uploaded_file:
            consideration_instance.consideration_filename = uploaded_file.name
            consideration_instance.consideration_data = uploaded_file.read()
        else:
            raise forms.ValidationError("No file uploaded.")
        consideration_instance.is_approved = False  # Definir como não aprovado por padrão
        if commit:
            consideration_instance.save()
        return consideration_instance
