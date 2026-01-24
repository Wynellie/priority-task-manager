from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    STATUS_CHOICES = [
        ('NS', 'Не начато'),
        ('IP', 'В работе'),
        ('DN', 'Сделано'),
    ]

    PRIORITY_CHOICES = [
        ('L','Низкий'),
        ('M', 'Средний'),
        ('H', 'Высокий'),

    ]

    title = models.CharField(max_length=255,verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    date = models.DateTimeField(auto_now_add=True,verbose_name='Дата')
    deadline = models.DateTimeField(verbose_name='Дедлайн')
    priority = models.CharField(max_length=1, choices = PRIORITY_CHOICES, default='M',verbose_name='Приоритет')
    status = models.CharField(max_length=2, choices= STATUS_CHOICES, default='NS',verbose_name='Статус')
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Пользователь',null=True, blank=True)

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-priority', 'deadline']

    def __str__(self):
        return self.title