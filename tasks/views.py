from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django import views
from .models import Task
from .forms import TaskForm

class IndexView(LoginRequiredMixin, views.View):
    # Сначала LoginRequiredMixin проверяет request.user.is_authenticated (до вызова get)
    # если False - redirect на LOGIN_URL в настройках

    # через AuthenticationMiddleware в каждом request есть user

    def get(self,request):
        tasks = Task.objects.filter(user = request.user)
        context = {
            'tasks': tasks,
            # форма задачи из forms.py - пустая, новая
            'form':TaskForm(),
        }
        return render(request,'tasks/index.html', context)

    def post(self,request):
        form = TaskForm(request.POST)
        # сверяет, можно ли записать в БД
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('index')

        context = {
            'tasks': Task.objects.filter(user=request.user),
            'form': form,
        }

        return render(request, 'tasks/index.html', context)

class DetailedView(views.View):

    def get(self,request,pk):
        task = get_object_or_404(Task,pk=pk,user=request.user)
        form = TaskForm(instance=task)
        context = {
            'task':task,
            'form':form,
        }
        return render(request, 'tasks/detailed.html',context)

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk,user=request.user)
        form = TaskForm(request.POST,instance=task)

        if form.is_valid():
            form.save()
            messages.success(request,'Задача обновлена!')
            return redirect('detailed',pk)

        context = {
            'form':form,
            'task':task,
        }
        return render(request,'tasks/detailed.html',context = context)


class Delete(LoginRequiredMixin, views.View):
    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)

        if request.user == task.user:
            task.delete()
            messages.success(request,'Задача удалена!')

        return redirect('index')



class RegisterView(views.View):
    def get(self,request):
        context = {
            'form':UserCreationForm()
        }
        return render(request,'tasks/auth.html',context=context)

    def post(self,request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
        context = {
            'form':form
        }
        return render(request,'tasks/auth.html',context)