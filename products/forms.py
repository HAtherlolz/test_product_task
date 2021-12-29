from django import forms

from .models import Comment, ShopCart


class CommentForm(forms.ModelForm):
    """ Comment form """
    class Meta:
        model = Comment
        fields = ("text",)


class ShopCartForm(forms.ModelForm):
    """ Shop Cart form """
    class Meta:
        model = ShopCart
        fields = ("amount",)