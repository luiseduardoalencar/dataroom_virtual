from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import File, Consideration, User
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    representative_name = forms.CharField(
        max_length=255, 
        required=True, 
        label='Nome do Representante',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Representante'})
    )
    position = forms.CharField(
        max_length=255, 
        required=True, 
        label='Cargo',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo'})
    )
    is_moderator = forms.BooleanField(required=False, label='Moderador')  # Novo campo

    class Meta:
        model = User
        fields = [
            'company_name', 'cnpj', 'social_reason', 'phone', 'email', 'address',
            'representative_name', 'position', 'is_moderator', 'password1', 'password2'  # Novo campo
        ]
        labels = {
            'company_name': 'Nome da Empresa',
            'cnpj': 'CNPJ',
            'social_reason': 'Razão Social',
            'phone': 'Telefone',
            'email': 'Email',
            'address': 'Endereço',
            'password1': 'Senha',
            'password2': 'Confirmação de Senha',
        }
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000000000000'}),
            'social_reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razão Social'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 0000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'representative_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Representative name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'}),
            'is_moderator': forms.CheckboxInput(attrs={'class': 'form-check-input'})  # Novo campo
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
        user.is_moderator = self.cleaned_data.get('is_moderator', False)  # Novo campo
        user.is_approved = False  
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
        fields = ['file', 'display_name', 'description', 'classification']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'classification': forms.Select(attrs={'class': 'form-control'}),
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
    is_approved = forms.BooleanField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Consideration
        fields = ['consideration_file', 'is_approved']

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

class AdminUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'is_admin', 'is_moderator', 'company_name', 'cnpj', 'social_reason', 'phone', 'address', 'representative_name', 'position')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
