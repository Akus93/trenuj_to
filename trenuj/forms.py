from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import Shortcut, Category, UserImage, Article
from django.contrib.auth.forms import PasswordChangeForm
from django.template.defaultfilters import slugify
from uuid import uuid4
from django.core.files.base import ContentFile
from embed_video.fields import EmbedVideoFormField


class SignupForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': "Hasła nie są takie same.",
    }
    username = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Powtórz hasło'
        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['first_name'].label = 'Imię'
        self.fields['last_name'].label = 'Nazwisko'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class LinkCreateForm(forms.ModelForm):

    class Meta:
        model = Shortcut
        exclude = ['author', 'type']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0, label='Kategoria')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': "materialize-textarea"}),
                                  max_length=256, label='Opis')
    image = forms.ImageField('Obrazek')
    link = forms.URLField()

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(LinkCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        shortcut = super(LinkCreateForm, self).save(commit=False)
        shortcut.author = User.objects.get(id=self.author)
        shortcut.type = 'link'
        if commit:
            shortcut.save()
        return shortcut


class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Shortcut
        fields = ['title', 'category', 'video']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0, label='Kategoria')
    video = EmbedVideoFormField()

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(VideoCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        shortcut = super(VideoCreateForm, self).save(commit=False)
        shortcut.author = User.objects.get(id=self.author)
        shortcut.type = 'video'
        if commit:
            shortcut.save()
        return shortcut


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Shortcut
        exclude = ['author', 'link', 'type']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0, label='Kategoria')
    description = forms.CharField(widget=forms.Textarea(attrs={'class': "materialize-textarea"}),
                                  max_length=256, label='Opis')
    image = forms.ImageField(label='Obrazek')

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(ImageCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        shortcut = super(ImageCreateForm, self).save(commit=False)
        shortcut.author = User.objects.get(id=self.author)
        shortcut.type = 'image'
        if commit:
            shortcut.save()
        return shortcut


class ChangePasswordForm(PasswordChangeForm):
    pass


class ProfileImageChangeForm(forms.ModelForm):

    class Meta:
        model = UserImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        circle_img = kwargs.pop('circle_image', None)
        self.circle_image = ContentFile(circle_img, '{}.png'.format(uuid4()))
        super(ProfileImageChangeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        old = UserImage.objects.filter(user=self.user).count()
        if old:
            change_image = UserImage.objects.get(user=self.user)
            change_image.image.delete(False)
            change_image.image = self.circle_image
            change_image.save()
            return change_image
        else:
            profile_image = super(ProfileImageChangeForm, self).save(commit=False)
            profile_image.image = self.circle_image
            profile_image.user = User.objects.get(id=self.user)
            if commit:
                profile_image.save()
            return profile_image


class ArticeCreateForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ArticeCreateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        article = super(ArticeCreateForm, self).save(commit=False)
        article.author = User.objects.get(id=self.user)
        article.slug = slugify(self.cleaned_data['title'])
        if commit:
            article.save()
        return article
