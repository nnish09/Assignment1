from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login, authenticate,logout,update_session_auth_hash
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from reglogprofile.models import User
from .forms import SignUpForm,SetPasswordForm,LoginForm,UpdateProfile
import json
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm


def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')


def account_activated(request):
    return render(request, 'account_activated.html')

def passwordsetdone(request):
    return render(request, 'passwordsetdone.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            user= form.save(commit=False)
            # user.refresh_from_db()  # load the profile instance created by the signal
            user.phone_no = form.cleaned_data.get('phone_no')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)) ,
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
          
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:      
        form = SignUpForm()
        
    return render(request, 'registration/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('setpassword',args=(uid,)))
    else:
        return HttpResponse('Activation link is expired!')

def setpassword(request,uid):
    if request.method=='POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=uid)
            password=request.POST.get('password')
            password = form.cleaned_data['password']
            confirm_password=request.POST.get('confirm_password')
            confirm_password = form.cleaned_data['confirm_password']
         
            # print(password)
            # a=User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            # print(user.password)
            # login(request, user)
            return redirect('passwordsetdone')

            
    else:
        form = SetPasswordForm()

    return render(request,"passwordset.html",{'form':form})

# # def login(request):
# #     return render(request,'registration/login.html')
# def login_user(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         # print(request.POST)
#         if login_form.is_valid:
#             username = request.POST.get('username')
#             # print(username)
#             password = request.POST.get('password')
#             username = login_form.cleaned_data['username']
#             password = login_form.cleaned_data['password']

#             # print(password)
            
#             user = authenticate(request,username=username, password=password)
#             print(user)
#             print(user.is_staff)

#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('home')
                    
#         else:
#             login_form = LoginForm()

#         return render(request, 'registration/c.html', {'login_form': login_form})

@login_required
def get_user_profile(request):
    user=request.user
    users = User.objects.all()
    return render(request, 'profile.html', {"users":users})

    
@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UpdateProfile(request.POST, request.FILES , instance=request.user)
        
        if (user_form.is_valid()):
           
            user_form.save()            
            return HttpResponseRedirect(reverse('profile'))
        
    else:
        user_form = UpdateProfile(instance=request.user)
    return render(request, 'registration/update_profile.html', {
        'user_form': user_form
    })




def change_password_done(request):
    return render(request, 'registration/password_changed.html')



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('passwordchanged')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form})