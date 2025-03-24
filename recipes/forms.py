from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from .models import Recipe, Review

class CustomLoguinForm(AuthenticationForm):
    username = forms.CharField(label="ユーザー名")


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'instructions', 'ingredients']
        exclude = ['user'] 
        wigets = {
        'instructions': forms.Textarea(attrs={'rows': 6, 'cols': 50}),
        'ingredients': forms.Textarea(attrs={'rows': 6, 'cols': 50}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        labels = {
            'comment':'コメント',
            'rating':'評価(1~5)',
        }


class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='検索キーワード', max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder':'レシピを検索'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        

