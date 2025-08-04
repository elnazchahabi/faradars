from django import forms
from .models import Comment, NewsletterSubscription

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control','rows':4,'placeholder':'نظر شما…'})
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل شما…'})}