from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'text': 'Пишите что-нибудь приятное, пожалуйста ^-^',
            'group': 'Выберите группу',
            'image': 'Ваше изображение будет показано в разрешении 1280x420'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
