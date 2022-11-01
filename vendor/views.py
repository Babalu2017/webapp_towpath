from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
from .forms import VendorForm
from accounts.forms import UserProfileForm

from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from my_shop.models import Category, ProductItem
from my_shop.forms import CategoryForm, ProductItemForm
from django.template.defaultfilters import slugify


#  helper
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vendorDashboard')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance = profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def myshop_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/myshop_builder.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def myshopitems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    shopitems = ProductItem.objects.filter(vendor=vendor, category=category)
    context = {
        'shopitems': shopitems,
        'category': category,
    }
    print(shopitems)
    return render(request, 'vendor/myshopitems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            
            category.save() # here the category id will be generated
            category.slug = slugify(category_name)+'-'+str(category.id) # chicken-15
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('myshop_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('myshop_builder')
        else:
            print(form.errors)

    else:
        form = CategoryForm(instance=category)
        
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('myshop_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_item(request):
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES)
        if form.is_valid():
            item_title = form.cleaned_data['item_title']
            item = form.save(commit=False)
            item.vendor = get_vendor(request)
            item.slug = slugify(item_title)+'-'+str(item.id) 
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('myshopitems_by_category', item.category.id)
        else:
            print(form.errors)

    else:
        form = ProductItemForm()
        # modify this form and get only the categories of the current vendor logged
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
    }
    return render(request, 'vendor/add_item.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_item(request, pk=None):
    item = get_object_or_404(ProductItem, pk=pk)
    if request.method == 'POST':
        form = ProductItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item_title = form.cleaned_data['item_title']
            item = form.save(commit=False)
            item.vendor = get_vendor(request)
            item.slug = slugify(item_title)
            item.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('myshopitems_by_category', item.category.id)
        else:
            print(form.errors)

    else:
        form = ProductItemForm(instance=item)
        # modify this form and get only the categories of the current vendor logged
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form': form,
        'item': item,
    }
    return render(request, 'vendor/edit_item.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_item(request, pk=None):
    item = get_object_or_404(ProductItem, pk=pk)
    item.delete()
    messages.success(request, 'Item has been deleted successfully!')
    return redirect('myshopitems_by_category', item.category.id)
