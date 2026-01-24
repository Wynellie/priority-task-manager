from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Какие поля отображать в списке
    list_display = ('title', 'status', 'priority', 'deadline')
    # По каким полям можно фильтровать
    list_filter = ('status', 'priority')
    # Поиск по заголовку
    search_fields = ('title',)