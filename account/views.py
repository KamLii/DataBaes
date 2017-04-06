from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse


from account.forms import UserRegistrationForm, UserProfileForm


# Create your views here.
class UserRegistrationFormView(View):
    form_class = UserRegistrationForm
    form2_class = UserProfileForm
    template_name = 'register/registration_form.html'

    # Displays blank form 
    def get(self, request):
        user_form = self.form_class(None)
        profile_form = self.form2_class(None)
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})

    # Process form data
    def post(self, request):
        
        user_form = self.form_class(request.POST)
        profile_form = self.form2_class(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(password)
            user.save()
            
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
    
            # Returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Grab user session info
                    # name = request.user.username
                    return redirect('/accounts/register/complete')
            else:
                HttpResponse("Invalid Login")
        
        return render(request, self.template_name, {'user_form': user_form, 'profile_form': profile_form})


class LoginView(View):
    template_name = 'login/login_form.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('homepage')
            else:
                return HttpResponse("BANNED")
        else:
            return HttpResponse("Invalid login details supplied.")

    def get(self, request):
        return render(request, self.template_name)


def logoutView(self, request):
    logout(request)
    return redirect('homepage')