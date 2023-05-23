from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from . forms import PasswordResetForm
from . models import *
import random
from django.db.models import Q



# For Code Generator
def create_code(name):
    name_parts = name.strip().split()
    first_letter = name_parts[0][0].upper() if name_parts else "X"
    last_letter = name_parts[-1][0][0].upper() if len(name_parts) > 1 else "X"
    random_numbers = str(random.randint(0, 99)).zfill(2)
    code = first_letter + last_letter + random_numbers
    return code


# Index
def index(request):
    return render(request, 'pages/index.html')


# Auth Login
def user_login(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
        
    return render(request, 'pages/auth/login.html')


# Password Reset
def PasswordReset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if password == confirm_password:
                try:
                    user = User.objects.get(username=username)
                    user.password = make_password(password)
                    user.save()
                    messages.success(request, "Password reset successful. Please login with your new password.")
                    return redirect('Login')
                except User.DoesNotExist:
                    messages.error(request, "User does not exist.")
            else:
                messages.error(request, "Passwords do not match. Please try again.")
    else:
        form = PasswordResetForm()

    context = {
        'form': form
    }

    return render(request, 'pages/auth/password_reset.html', context)


# Logout
def logout_from_dashbaord(request):
    logout(request)
    return redirect('login')


# Dashboard
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'pages/dashboard/dashboard.html')


# Parent Category View
@login_required(login_url='login')
def parent_category(request):
    parent_category_details = ParentCategory.objects.all()

    # Pagination
    paginator = Paginator(parent_category_details, 5)  # Show 5 records per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the current page object

    # Search
    search_query = request.GET.get('search')

    if search_query:
        parent_category_details = parent_category_details.filter(
            Q(name__icontains=search_query) | Q(code__icontains=search_query) | Q(id__icontains=search_query)
        )

    context = {
        'parent_category_details': page_obj,
        'search_query': search_query,
    }

    return render(request, 'components/categories/parent_category.html', context)


# Add Parent Category
@login_required(login_url='login')
def add_parent_category(request):
    if request.method == 'POST':
        name = request.POST.get('parent_category_name')
        icon = request.FILES.get('parent_category_icon')
        code = create_code(name)

        if ParentCategory.objects.filter(name=name).exists():
            messages.error(request, "Category Already Exists")
        else:
            try:
                category = ParentCategory(name=name, icon=icon, code=code)
                category.save()
                messages.success(request, "Category Created")
            except Exception as e:
                messages.error(request, str(e))
                
    return redirect('parent_category')


# Update Parent Category
@login_required(login_url='login')
def update_parent_category(request, id):
    # Get the ID
    id = id

    if request.method == "POST":
        name = request.POST.get('edit_parent_category_name')
        is_active = request.POST.get('edit_parent_category_status') == 'on'

        if not ParentCategory.objects.filter(id=id).exists():
            messages.error(request, "Category Does Not Exist")
        else:
            try:
                parent_category = ParentCategory.objects.get(id=id)
                parent_category.name = name
                parent_category.is_active = is_active
                parent_category.save()
                messages.success(request, "Category Updated Successfully")
            except Exception as e:
                messages.error(request, "Error Updating Category: " + str(e))

    return redirect('parent_category')


# Delete Parent Category
@login_required(login_url='login')
def delete_parent_category(request, id):
    try:
        category = ParentCategory.objects.get(id=id)
        category.delete()
        messages.success(request, "Deleted Successfully")
    except ParentCategory.DoesNotExist:
        pass

    return redirect('parent_category')


# Sub Category View
@login_required(login_url='login')
def sub_category(request):
    sub_category_details = SubCategory.objects.all()

    # Get the Parent Category Details like ID and Name
    parent_category_menu_list = ParentCategory.objects.values('code', 'name')

    # Pagination
    paginator = Paginator(sub_category_details, 5)  # Show 5 records per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the current page object

    # Search
    search_query = request.GET.get('search')

    if search_query:
        sub_category_details = sub_category_details.filter(
            Q(name__icontains=search_query) | Q(code__icontains=search_query) | Q(id__icontains=search_query)
        )

    context = {
        'sub_category_details': page_obj,
        'search_query': search_query,
        'parent_category_menu_list': parent_category_menu_list,
    }

    return render(request, 'components/categories/sub_category.html', context)


# Add Sub Category
@login_required(login_url='login')
def add_sub_category(request):
    if request.method == "POST":
        parent_category_code = request.POST.get('parent_category_id')
        parent_category_name = ParentCategory.objects.get(code=parent_category_code)
        sub_category_name = request.POST.get('sub_category_name')
        code = create_code(sub_category_name)
        final_code = parent_category_code + code

        if SubCategory.objects.filter(name=sub_category_name).exists():
            messages.error(request, "Category Already Exists")
        else:
            try:
                category = SubCategory(category=parent_category_name, name=sub_category_name, code=final_code)
                category.save()
                messages.success(request, "Category Created")
            except Exception as e:
                messages.error(request, e)

    return redirect('sub_category')


# Update Sub Category
@login_required(login_url='login')
def update_sub_category(request, id):
    # Get the ID
    id = id

    if request.method == "POST":
        name = request.POST.get('edit_sub_category_name')
        is_active = request.POST.get('edit_sub_category_status') == 'on'

        if not SubCategory.objects.filter(id=id).exists():
            messages.error(request, "Category Does Not Exist")
        else:
            try:
                sub_category = SubCategory.objects.get(id=id)
                sub_category.name = name
                sub_category.is_active = is_active
                sub_category.save()
                messages.success(request, "Category Updated Successfully")
            except Exception as e:
                messages.error(request, "Error Updating Category: " + str(e))

    return redirect('sub_category')


# Delete Sub Category
@login_required(login_url='login')
def delete_sub_category(request, id):
    try:
        category = SubCategory.objects.get(id=id)
        category.delete()
        messages.success(request, "Deleted Successfully")
    except SubCategory.DoesNotExist:
        pass

    return redirect('sub_category')


# Location
@login_required(login_url='login')
def location(request):
    all_location_names = Location.objects.all()

    # Pagination
    paginator = Paginator(all_location_names, 5)  # Show 5 records per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the current page object

    # Search
    search_query = request.GET.get('search')

    if search_query:
        all_location_names = all_location_names.filter(
            Q(name__icontains=search_query) | Q(id__icontains=search_query) | Q(id__icontains=search_query)
        )

    context = {
        'all_location_names': page_obj,
        'search_query': search_query,
    }

    return render(request, 'components/location.html', context)


# Add Location
@login_required(login_url='login')
def add_location(request):
    if request.method == "POST":
        location_name = request.POST.get('location_name')

        if Location.objects.filter(name=location_name).exists():
            messages.error(request, "Location Already Exist")
        else:
            try:
                name_of_location = Location(name=location_name)
                name_of_location.save()
                messages.success(request, "Location Added")
            except Exception as e:
                messages.error(request, e)

    return redirect('location')


# Update Location
@login_required(login_url='login')
def update_location(request, id):
    # Get the ID
    id = id

    if request.method == "POST":
        name = request.POST.get('edit_Location_name')
        is_active = request.POST.get('edit_location_status') == 'on'

        if not Location.objects.filter(id=id).exists():
            messages.error(request, "Location Does Not Exist")
        else:
            try:
                location_data = Location.objects.get(id=id)
                location_data.name = name
                location_data.is_active = is_active
                location_data.save()
                messages.success(request, "Location Updated Successfully")
            except Exception as e:
                messages.error(request, "Error Updating Location: " + str(e))

    return redirect('location')


# Delete Location
@login_required(login_url='login')
def delete_location(request, id):
    try:
        location_data = Location.objects.get(id=id)
        location_data.delete()
        messages.success(request, "Deleted Successfully")
    except Location.DoesNotExist:
        pass

    return redirect('location')


# User Role
def user_role(request):
    all_group_names = UserRole.objects.all()

    # Pagination
    paginator = Paginator(all_group_names, 5)  # Show 5 records per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the current page object

    # Search
    search_query = request.GET.get('search')

    if search_query:
        all_group_names = all_group_names.filter(
            Q(name__icontains=search_query) | Q(id__icontains=search_query) | Q(id__icontains=search_query)
        )

    context = {
        'all_group_names': page_obj,
        'search_query': search_query,
    }

    return render(request, 'components/groups.html', context)


# User Role
def add_user_role(request):
    if request.method == "POST":
        group_name = request.POST.get('group_name')

        if UserRole.objects.filter(name=group_name).exists():
            messages.error(request, "Group Already Exist")
        else:
            try:
                name_of_location = UserRole(name=group_name)
                name_of_location.save()
                messages.success(request, "Group Added")
            except Exception as e:
                messages.error(request, e)

    return redirect('user_role')


# User Role
def update_user_role(request, id):
    # Get the ID
    id = id

    if request.method == "POST":
        name = request.POST.get('edit_group_name')
        is_active = request.POST.get('edit_group_status') == 'on'

        if not UserRole.objects.filter(id=id).exists():
            messages.error(request, "Group Does Not Exist")
        else:
            try:
                user_role_data = UserRole.objects.get(id=id)
                user_role_data.name = name
                user_role_data.is_active = is_active
                user_role_data.save()
                messages.success(request, "Group Updated Successfully")
            except Exception as e:
                messages.error(request, "Error Updating Group: " + str(e))

    return redirect('user_role')


# User Role
def delete_user_role(request, id):
    try:
        group_data = UserRole.objects.get(id=id)
        group_data.delete()
        messages.success(request, "Deleted Successfully")
    except Location.DoesNotExist:
        pass
    return redirect('user_role')