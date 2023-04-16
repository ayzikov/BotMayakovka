from .models import Piece
from django import forms
class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ('id', 'name', 'date', 'genre', 'description')
        widgets = {
            'name': forms.TextInput(),
            'date': forms.NumberInput(),
            'genre': forms.TextInput(),
        }