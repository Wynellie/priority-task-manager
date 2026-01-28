from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django import views
from .models import Task
from .forms import TaskForm

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class IndexView(LoginRequiredMixin, views.View):
    def get(self,request):
        context = {
            'tasks': Task.objects.filter(user = request.user),
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
            if is_ajax(request):
                return JsonResponse({
                    'status' : 'ok',
                    'message' : 'Задача добавлена!',
                })
            # в случае, если запрос не через js
            return redirect('index')

        context = {
            'tasks': Task.objects.filter(user=request.user),
            'form': form,
        }
        return render(request, 'tasks/index.html', context)

class DetailedView(LoginRequiredMixin, views.View):
    def get(self,request,pk):
        task = get_object_or_404(Task,pk=pk,user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tasks/detailed.html',{'task':task,'form':form})

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk,user=request.user)
        form = TaskForm(request.POST,instance=task)

        if form.is_valid():
            form.save()
            if is_ajax(request):
                return JsonResponse({
                    'status' : 'ok',
                    'message' : 'Задача обновлена',
                })
            return redirect('detailed',pk)

        context = {
            'form':form,
            'task':task,
        }
        return render(request,'tasks/detailed.html',context = context)


class Delete(LoginRequiredMixin, views.View):
    def post(self,request,pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()

        if is_ajax(request):
            return JsonResponse({
                'status': 'ok',
                'message': 'Задача удалена!'
            })

        return redirect('index')

class RegisterView(views.View):
    def get(self,request):
        return render(request,'tasks/auth.html', {'form':UserCreationForm()})

    def post(self,request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
        return render(request,'tasks/auth.html',{'form':form})