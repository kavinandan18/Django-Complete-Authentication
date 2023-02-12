from django.shortcuts import render
from django.contrib.auth.views import (
    LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,
    PasswordResetCompleteView,LogoutView,PasswordChangeDoneView
)
from accounts.forms import (Signupform,LoginForm,UserEditForm,ProfileEditForm,
ChangePasswordForm,PasswordResetEmailForm,NewSetPasswordForm)
from django.views.generic import CreateView,View
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from.models import Profile
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class SignupCreateView(CreateView):
    form_class = Signupform
    template_name = 'accounts/signup.html'
    success_url = 'login'


# views.py of the accounts app


class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    #success_url = settings.LOGIN_REDIRECT_URL
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().form_valid(form)


class UserLogOutViews(LogoutView):
    template_name='accounts/logout.html'

   
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class ProfileUpdateView(LoginRequiredMixin,View):
    login_url = 'login'

    def get(self,request):
        u_form = UserEditForm(instance= request.user)
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
        p_form = ProfileEditForm(instance= profile)

        context = { 
            'u_form':u_form,
            'p_form':p_form
        }
        return render(request, 'accounts/profile_edit.html',context)

    def post(self,request):
        u_form = UserEditForm(request.POST,instance= request.user)
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
        p_form = ProfileEditForm(request.POST,request.FILES,instance= profile)

        if u_form.is_valid() and p_form.is_valid():
            print(u_form.cleaned_data)
            print(p_form.cleaned_data)
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')

        context = { 
            'u_form':u_form,
            'p_form':p_form
        }
        return render(request, 'accounts/profile_edit.html',context)


class Password_Reset_View(PasswordResetView):
    template_name='accounts/password_reset_form.html'
    email_template_name='accounts/password_reset_email.html'
    form_class = PasswordResetEmailForm


class Password_Reset_Done_View(PasswordResetDoneView):
    template_name= 'accounts/password_reset_done.html'


class Password_Reset_Confirm_View(PasswordResetConfirmView):
    template_name= 'accounts/password_confirm.html'
    form_class = NewSetPasswordForm


class Password_Reset_Complete_View(PasswordResetCompleteView):
    template_name= 'accounts/password_reset_complete.html'




class Password_Change_View(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/password_change_form.html'

    def get(self, request):
        form = ChangePasswordForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully changed!')
            update_session_auth_hash(request, form.user) # Add this line
            return redirect('password_change_done')
        else:
            return render(request, self.template_name, {'form': form})



class Password_Change_Done_Views(PasswordChangeDoneView):
    template_name= 'accounts/password_change_done.html'