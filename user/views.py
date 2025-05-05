from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignupForm
from .factory import UserFactory
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = UserFactory.create_user(form)
            login(request, user)
            return redirect('app:home')
    else:
        form = UserSignupForm()
    
    return render(request, 'user/signup.html', {'form': form})

class MyLoginView(LoginView):
    template_name = 'user/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == 'Donor':
            return reverse_lazy('donation:donate_food')
        elif user.role == 'Recipient':
            return reverse_lazy('donation:view_donation')
        elif user.role == 'Driver':
            return reverse_lazy('delivery:available_delivery')
        elif user.is_superuser:
            return reverse_lazy('admin:index')
        return reverse_lazy('app:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
