from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserImageForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth import authenticate,login,logout
from .models import UserImageModel
import numpy as np
from tensorflow import keras
from PIL import Image,ImageOps




def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

from .models import Profile

def profile(request):
    user = request.user
    # Ensure the user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from . models import UserImageModel
from . import forms
from .forms import UserImageForm


def Deploy_8(request): 
    print("HI")
    if request.method == "POST":
        form = forms.UserImageForm(files=request.FILES)
        if form.is_valid():
            print('HIFORM')
            form.save()
        obj = form.instance

        result1 = UserImageModel.objects.latest('id')
        models = keras.models.load_model('E:/IYYAPPAN/ITPDL10-FINAL/ITPDL10-FINAL CODE/Deploy/Project/App/Model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open("E:/IYYAPPAN/ITPDL10-FINAL/ITPDL10-FINAL CODE/Deploy/Project/" + str(result1)).convert("RGB")
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        classes = ["AnnualCrop","Bridge aerial","Damage","Forest","Highway","Industrial aerial","Industrial sat",
                  "Intersection aerial","Landmark aerial","Park aerial","Parking aerial","PermanentCrop",
                  "Playground aerial","Residential aerial","Residential","River","SeaLake","Shipsnet",
                  "Stadium aerial","Waterbodies"]
        prediction = models.predict(data)
        idd = np.argmax(prediction)
        a = (classes[idd])
        if a == "AnnualCrop":
             b ='AnnualCrop'
        elif a == "Bridge aerial":
            b ='Bridge aerial'
        elif a == "Damage":
            b ='Damage'
        elif a == "Forest":
            b ='Forest'
        elif a == "Highway":
            b ='Highway'
        elif a == "Industrial aerial":
            b ='Industrial aerial'
        elif a == "Industrial sat":
            b ='Industrial sat'
        elif a == "Intersection aerial":
            b ='Intersection aerial'
        elif a == "Landmark aerial":
           b ='Landmark aerial'
        elif a == "Park aerial":
            b ='Park aerial'
        elif a == "Parking aerial":
            b ='Parking aerial'
        elif a == "PermanentCrop":
            b ='PermanentCrop'
        elif a == "Playground aerial":
            b ='Playground aerial'
        elif a == "Residential aerial":
            b ='Residential aerial'
        elif a == "Residential":
            b ='Residential'
        elif a == "River":
            b ='River'
        elif a == "SeaLake":
            b ='SeaLake'
        elif a == "Shipsnet":
            b ='Shipsnet'
        elif a == "Stadium aerial":
            b ='Stadium aerial'
        elif a == "Waterbodies":
            b ='Waterbodies'
        else:
            b = 'WRONG INPUT'

        data = UserImageModel.objects.latest('id')
        data.label = a
        data.save()

        
        # text_to_speech(a, delay=7)

        
        return render(request, 'App/output.html',{'form':form,'obj':obj,'predict':b})
    else:
        
        form = forms.UserImageForm()
    return render(request, 'App/model.html',{'form':form})


# import pyttsx3
# import time

# def text_to_speech(text, delay=7):
#     time.sleep(delay)
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()

def Database(request):
    models = UserImageModel.objects.all()
    return render(request, 'App/Database.html', {'models': models})


def logout_view(request):  
    auth_logout(request)
    return redirect('/')