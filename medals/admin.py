from django.contrib import admin
from .models import Rank, Status, Category, Documents, Medal, Soldier
# Register your models here.


admin.site.register([Rank, Status, Category, Documents, Medal])

@admin.register(Soldier)
class PostAdmin(admin.ModelAdmin):
    list_display = ('status', 'rank', 'F', 'I', 'O')
    list_filter = ('status', 'rank')
    search_fields = ('status', 'rank')
    ordering = ('F', 'I')
