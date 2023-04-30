from .models import Piece
from django import forms
class PieceForm(forms.ModelForm):
    class Meta:
        model = Piece
        fields = ('id',
                  'name',
                  'date',
                  'genre',
                  'little_known',
                  'description_piece',
                  'description_piece_detailed',
                  'description_play',
                  'link_play',
                  'link_video',
                  'image')

        widgets = {
            'name': forms.TextInput(),
            'date': forms.NumberInput(),
            'genre': forms.TextInput(),
            'description_piece': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'description_piece_detailed': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'description_play': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'link_play': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
            'link_video': forms.Textarea(attrs={'rows': 6, 'cols': 60})
        }