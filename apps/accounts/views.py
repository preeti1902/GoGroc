from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..base.models import Profile
from ..base.emails import sendAccountActivationEmail
import uuid
from .emails import sendPasswordResetEmail

def registerView(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        userObj = User.objects.filter(username = email)
        if userObj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)
        userObj = User.objects.create(first_name = firstName , last_name = lastName , email = email , username = email)
        userObj.set_password(password)
        userObj.save()
        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)
    return render(request ,'accounts/register.html')

def loginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        userObj = User.objects.filter(username=email)
        if not userObj.exists():
            messages.warning(request, "Account not found")
            return HttpResponseRedirect(request.path_info)
        user = userObj[0]
        if not userObj[0].profile.isEmailVerified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)
        if user.profile.isEmailVerified:
            userObj = authenticate(username=email, password=password)
            if userObj:
                login(request, userObj)
                return HttpResponseRedirect('/')
            messages.warning(request, "Invalid Credentials")
            return HttpResponseRedirect(request.path_info)
        else:
            emailToken = str(uuid.uuid4())
            profile = Profile.objects.create(user=user, emailToken=emailToken)
            sendAccountActivationEmail(email, emailToken)
            messages.warning(request, 'Please verify your email before logging in. Activation email sent.')
            return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')

def emailActivationView(request, emailToken):
    try:
        user = Profile.objects.get(emailToken=emailToken)
        user.isEmailVerified = True
        user.save()
        messages.success(request, 'Email Is Verified, Please Login')
        return redirect('/')
    except Profile.DoesNotExist:
        print(f'Invalid Email Token: {emailToken}')
        return HttpResponse('Invalid Email Token')

@login_required
def logoutView(request):
    logout(request)
    return redirect('/')

# password reset
def passwordResetView(request, token):
    context = {}
    try:
        profileObj = Profile.objects.get(forgetPasswordToken = token)
        context = {'user_id':profileObj.user.id}
        if request.method == 'POST':
            newPassword = request.POST.get('new_password')
            confirmPassword = request.POST.get('confirm_password')
            userId = request.POST.get('user_id')
            if userId is None:
                messages.warning(request, 'No user id found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if newPassword != confirmPassword:
                messages.warning(request, 'Confirm Password Does not match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            userObj = User.objects.get(id = userId)
            userObj.set_password(newPassword)
            userObj.save()
            return redirect('login')
    except Exception as e:
        print(e)
    return render(request, 'accounts/reset_password.html',context)

def forgotPasswordView(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not User.objects.filter(email=email).first():
                messages.error(request, 'User Not Found')
                return redirect('/forgot-password')
            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user = user_obj)
            profile_obj.forgetPasswordToken = token
            profile_obj.save()
            sendPasswordResetEmail(user_obj,token)
            messages.warning(request, 'Reset Password Link has been sent to your email')
            return redirect('forgot-password')
    except Exception as e:
        print(e)
    return render(request, 'accounts/forgot_password.html')