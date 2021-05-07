# Idealbreed-todo

**Install Django in your system (Windows)**
```
pip install django
```

**Create Project**
```
django-admin startproject TodoApp
```

**Create Django app**
```
django-admin startapp todo
```

## Editing setting
1. Add app name(i.e todo) to **INSTALLED_APP** in setting
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',
]
```
2. Edit directory path in TEMPLATES
```
'DIRS': [BASE_DIR / 'templates'],
```

### Extra file and folders you to create
1. - templates(Folder)
      - todo(Folder)
        - home.html (file)
        - update.html (file)
        - delete.html (file)
        - edit.html (file)

2. Create two file in **todo** app
    - urls.py
    - forms.py

### Create URLs for main project **TodoApp.urls.py**
```
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
]
```

### Create model
```
from django.db import models


# Create your models here.
class TodoModel(models.Model):
    title = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
 ```
 
 ### Writing in forms -- *forms.py*
 ```
   
from .models import TodoModel
from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = TodoModel
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Add task here...',
                }
            )
        }
```
 
 ### Register model in admin -- *todo/admin.py*
 ```
 from django.contrib import admin
from .models import TodoModel

# Register your models here.
admin.site.register(TodoModel)
```
 
 # Function to READ, WRITE, UPDATE & DELETE
 ### Read and Write Operations -- *todo/views.py*
 ```
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
```

### Update function -- *todo/views.py*
```
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
```

### Delete Function -- *todo/views.py*
```
def delete(request, id):
    item = TodoModel.objects.get(id=id)
    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {
        'item': item,
    }
    return render(request, 'todo/delete.html', context)
```


### Writing path for above functions -- *todo/urls.py*
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('update/<str:pk>/', views.update, name='update'),
]
```





# Rendering Templates
### templates/todo/base.html
```
<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Hello, TODO!</title>
</head>
<body>
<div class="d-flex justify-content-center m-4 ">
    <h1><a href="{% url 'home' %}" class="text-danger" style="text-decoration: none">Todo App</a></h1>
</div>
<div style="height: 2px;background-color: #1b1b1b;"></div>
{% block content %}
{% endblock content %}
<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
        crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
        integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
        crossorigin="anonymous"></script>
</body>
</html>
```

### templates/todo/home.html
```
{% extends 'todo/base.html' %}
{% block content %}

    <div class="d-flex justify-content-center mt-4">
        <div class="container">
            <form method="POST" action="/">
                {% csrf_token %}
                <div class="form-group row">
                    <div class="col">
                        {{ form.title }}
                    </div>
                </div>
                <div class="form-group row">
                    <div class="col">
                        <input type="submit" class="form-control btn-primary" value="ADD TASK">
                    </div>
                </div>
            </form>
        </div>
    </div>
    <hr>
    <hr>

    <div class="container">
        <table class="table table-striped table-dark">
            <tbody>
            {% for todo in todos %}
                <tr>
                    <td class="col-lg-8">{{ todo.title }}</td>
                    <td><a href="{% url 'update' todo.id %}" class="text-primary col-lg-2">Edit</a></td>
                    <td><a href="{% url 'delete' todo.id %}" class="text-danger col-lg-2">Delete</a></td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>

{% endblock content %}
```

### templates/todo/update.html 
```
{% extends 'todo/base.html' %}
{% block content %}
    <div class="d-flex justify-content-center mt-4">
        <div class="container">
            <form method="POST" action="">
                {% csrf_token %}
                <div class="form-group row">
                    <div class="col">
                        {{ form.title }}
                    </div>
                </div>
                <div class="form-group row">
                    <div class="col">
                        <input type="submit" class="form-control btn-primary" value="UPDATE TASK">
                    </div>
                </div>
            </form>
            <div class="d-flex justify-content-center mt-4">
                <a href="{% url 'home' %}">Cancel</a>
            </div>
        </div>
    </div>
{% endblock content %}
```


### templates/todo/delete.html
```
{% extends 'todo/base.html' %}
{% block content %}
    <div class="d-flex justify-content-center mt-4">
        <p>Are you sure you want to delete <strong>"{{ item }}"</strong> ?</p>
    </div>

    <div class="d-flex justify-content-center mt-4">
        <form action="" method="POST">
            {% csrf_token %}
            <div class="form-group row">
                <div class="col">
                    <input type="submit" name="Confirm" class="form-control btn-danger" value="Delete">
                </div>
            </div>
        </form>
    </div>

    <div class="d-flex justify-content-center mt-4">
        <a href="{% url 'home' %}">Cancel</a>
    </div>
{% endblock content %}
```


# Code to run Project Successfully
1. ```python manage.py makemigrations```
2. ```python manage.py migrate```
3. ```python manage.py runserver```
