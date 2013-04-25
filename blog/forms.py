from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext as _
from django.core.mail import send_mail


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    sender = forms.EmailField(required=False)
    subject = forms.CharField(max_length=100)
    message = forms.Field(widget=forms.Textarea)

    def send_email(self):
        subject = self.cleaned_data['subject']
        from_email = self.cleaned_data['sender']
        message = """
            Nome: %(name)s
            E-mail: %(sender)s
            Mensagem: %(message)s
        """ % self.cleaned_data

        send_mail(subject, message, from_email, ['brenotx@gmail.com'],)


class RegisterForm(forms.ModelForm):
    """Form for registering a new user account and validates fields"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    confirm_password = forms.CharField(
            max_length=30, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.base_fields['password'].help_text = 'Informe uma senha segura'
        self.base_fields['password'].widget = forms.PasswordInput()
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        """Validates the username as unique"""
        if User.objects.filter(username=self.cleaned_data['username']).count():
            raise forms.ValidationError('Ja existe um usuario com este username')

        return self.cleaned_data['username']

    def clean_email(self):
        """Validates the email as unique"""
        if User.objects.filter(email=self.cleaned_data['email']).count():
            raise forms.ValidationError('Ja existe um usuario com este email')

    def clean_confirm_password(self):
        """Validates the confirm password as iqual a previews password"""
        if self.cleaned_data['confirm_password'] != self.data['password']:
            raise form.ValidationError('Confirmacao de senha nao confere')

        return self.cleaned_data['confirm_password']

    def save(self, commit=True):
        """"""
        user = super(RegisterForm, self).save(commit=False)

        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user
