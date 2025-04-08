from django import forms
from .models import Review, Book

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'review_content']
        widgets = {
            'rate': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'review_content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'rate': 'Ocena (1–5)',
            'review_content': 'Treść recenzji',
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'description', 'category', 'cover']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Tytuł książki',
            'author': 'Autor',
            'description': 'Opis',
            'category': 'Kategoria',
            'cover': 'Okładka',
        }