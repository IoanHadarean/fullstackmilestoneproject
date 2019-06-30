from django import forms
from forum.models import Post, Comment

class PostForm(forms.ModelForm):
    """
    A form class that is connected to the Post model.
    Takes in a widgets dictionary for the Meta class
    that allows customizing different parts of the form.
    """
    
    class Meta():
        model = Post
        fields = ('author', 'title', 'text')
      
        widgets = {
            'title':forms.TextInput(attrs={'class': 'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
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
            'author':forms.TextInput(attrs={'class': 'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }