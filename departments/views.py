from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Department
from .forms import SignupForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user) 
        messages.success(self.request, f"Welcome, {user.username}!")  
        return super().form_valid(form)  

    def get_success_url(self):
        return reverse_lazy('department_list') 


def is_admin(user):
    return user.is_superuser

def signup(request):
    if request.method == "POST":
        form =SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful! You can now log in.")
            return redirect("login")  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()


    storage = messages.get_messages(request)
    storage.used = True  

    return render(request, 'signup.html', {'form': form})
    

@login_required(login_url='login')
def department_list(request):
    query = request.GET.get('q', '')  
    departments = Department.objects.filter(
        Q(dept_name__icontains=query) | Q(description__icontains=query),
        status=True  
    )
    return render(request, 'department_list.html', {'departments': departments, 'query': query})


@login_required(login_url='login')
@user_passes_test(is_admin)
def department_create(request):
    if request.method == "POST":
        dept_name = request.POST.get("dept_name")
        description = request.POST.get("description")
        
        if Department.objects.filter(dept_name=dept_name).exists():
            messages.error(request, "A department with this name already exists.")
            return render(request, 'department_form.html', {'dept_name': dept_name, 'description': description})

        Department.objects.create(dept_name=dept_name, description=description)
        messages.success(request, "Department created successfully!")
        return redirect('department_list')
    
    return render(request, 'department_form.html')


@login_required(login_url='login')
@user_passes_test(is_admin)
def department_update(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    if request.method == "POST":
        department.dept_name = request.POST.get("dept_name")
        department.description = request.POST.get("description")
        department.save()
        messages.success(request, "Department updated successfully!")
        return redirect('department_list')
    return render(request, 'department_form.html', {'department': department})


@login_required(login_url='login')
@user_passes_test(is_admin)
def department_delete(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    if request.method == "POST":
        department.status = False  
        department.save()
        messages.warning(request, "Department has been deactivated.")
        return redirect('department_list')

    return render(request, 'department_confirm_delete.html', {'department': department})






