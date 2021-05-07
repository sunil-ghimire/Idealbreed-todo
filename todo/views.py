from django.shortcuts import render, redirect
from .models import TodoModel
from .forms import TaskForm


# Create your views here.
def home(request):
    todos = TodoModel.objects.all()  # Getting all data from DB
    form = TaskForm()  # creating object from form(ModelForm)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    context = {
        'todos': todos,
        'form': form,
    }
    return render(request, 'todo/home.html', context)


def update(request, pk):
    task = TodoModel.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'todo/update.html', context)


def delete(request, id):
    item = TodoModel.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {
        'item': item,
    }
    return render(request, 'todo/delete.html', context)
