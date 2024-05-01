from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game, Profilis, Comment


class GameUploadForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'file', 'thumbnail', 'index_file']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'game', 'commenter')
        widgets = {'game': forms.HiddenInput(), 'commenter': forms.HiddenInput()}