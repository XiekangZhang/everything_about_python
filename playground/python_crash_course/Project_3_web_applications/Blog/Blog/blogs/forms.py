from django import forms
from .models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "text"]
        labels = {
            "title": "Title",
            "text": "Content"
        }
        #widgets = {"title", forms.TextInput(attrs={"cols": 80})}
