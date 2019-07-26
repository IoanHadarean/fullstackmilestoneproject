from django import forms
from django.shortcuts import get_object_or_404
from forum.models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    """
    A form class that is connected to the Post model.
    Takes in a widgets dictionary for the Meta class
    that allows customizing different parts of the form.
    The __init__ function is overwritten and the author field
    is filtered by the 'user.username' to prevent selecting from
    a dropdown of multiple users.
    """

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = User.objects.filter(username=user.username)


class PostEditForm(forms.ModelForm):
    """
    A form class that is connected to the Post model
    and allows editing a post. Takes in a widgets dictionary
    for the Meta class that allows customizing different parts
    of the form.
    """

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }


class CommentForm(forms.ModelForm):
    """
    A form class that is connected to the Comment model.
    Takes in a widgets dictionary for the Meta class
    that allows customizing different parts of the form.
    """

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
