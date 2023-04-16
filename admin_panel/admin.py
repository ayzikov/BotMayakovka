from django.contrib import admin
from .models import Piece
from .forms import PieceForm

@admin.register(Piece)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date', 'genre', 'description')
    form = PieceForm
