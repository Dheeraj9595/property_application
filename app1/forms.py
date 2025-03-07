from django import forms
from .models import Property, Owner  # Assuming User is your owner model

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'owner', 'area', 'property_type', 'property_subtype']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter property title'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter area'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'property_subtype': forms.Select(attrs={'class': 'form-control'}),
        }

    owner = forms.ModelChoiceField(
        queryset=Owner.objects.all(),  # Fetch all owners
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Owner"  # Placeholder text for dropdown
    )

