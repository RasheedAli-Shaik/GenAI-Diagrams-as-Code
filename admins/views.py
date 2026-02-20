from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import UserRegistrationModel


def adminLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginid')
        pswd = request.POST.get('password')

        if usrid == 'admin' and pswd == 'admin':
            request.session['admin_logged'] = True
            request.session['admin_user'] = 'Admin'
            return redirect('AdminHome')
        else:
            messages.error(request, 'Invalid login ID or password')
            return render(request, 'AdminLogin.html')

    return render(request, 'AdminLogin.html')

def adminHome(request):
    if not request.session.get('admin_logged'):
        messages.error(request, 'Please login as admin first.')
        return redirect('AdminLogin')
    return render(request, 'admins/AdminHome.html')

def adminLogout(request):
    request.session.flush()
    messages.success(request, 'Admin logged out successfully.')
    return redirect('index')

def RegisterUsersView(request):
    if not request.session.get('admin_logged'):
        messages.error(request, 'Please login as admin first.')
        return redirect('AdminLogin')
    data = UserRegistrationModel.objects.all()
    return render(request, 'admins/viewregister.html', {'data': data})


def activateUser(request):
    if not request.session.get('admin_logged'):
        return redirect('AdminLogin')
    if request.method == 'GET':
        uid = request.GET.get('uid')
        if uid:
            UserRegistrationModel.objects.filter(id=uid).update(status='activated')
            messages.success(request, 'User activated successfully.')
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/viewregister.html', {'data': data})
    return redirect('RegisterUsersView')


def DeactivateUsers(request):
    if not request.session.get('admin_logged'):
        return redirect('AdminLogin')
    if request.method == 'GET':
        uid = request.GET.get('uid')
        if uid:
            UserRegistrationModel.objects.filter(id=uid).update(status='deactivated')
            messages.success(request, 'User deactivated successfully.')
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/viewregister.html', {'data': data})
    return redirect('RegisterUsersView')


def deleteUser(request):
    if not request.session.get('admin_logged'):
        return redirect('AdminLogin')
    if request.method == 'GET':
        uid = request.GET.get('uid')
        if uid:
            UserRegistrationModel.objects.filter(id=uid).delete()
            messages.success(request, 'User deleted successfully.')
        data = UserRegistrationModel.objects.all()
        return render(request, 'admins/viewregister.html', {'data': data})
    return redirect('RegisterUsersView')
         