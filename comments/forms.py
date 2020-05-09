from django import forms
from .models import Comment


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class':'textAreaBox','placeholder':"Ask Something..."}),
        label=''
        )
