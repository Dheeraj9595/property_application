from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'user', 'student']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),  # HTML date picker
        }
