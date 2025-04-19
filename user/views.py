from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            role = form.cleaned_data['role']
            group = Group.objects.get(name=role)  # Ensure group exists in admin
            user.groups.add(group)

            login(request, user)
            return redirect('home')  # or any dashboard page
    else:
        form = UserSignupForm()
    return render(request, 'user/signup.html', {'form': form})

class MyLoginView(LoginView):
    template_name = 'user/login.html'  # Define the path to your custom login template

    def get_success_url(self):
        # Redirect based on user role or any custom logic
        if self.request.user.groups.filter(name='Donor').exists():
            return reverse_lazy('donation:donate_food')  # Redirect to donation page for Donors
        elif self.request.user.groups.filter(name='Recipient').exists():
            return reverse_lazy('donation:donation_list')  # Redirect to recipient's donations page
        elif self.request.user.is_superuser:
            return reverse_lazy('admin:index')  # Redirect to admin dashboard for superusers
        return reverse_lazy('home')  # Default redirect (can be the homepage)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = AuthenticationForm()  # Ensure the form is passed to the template
        return context
