from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from .forms import UserLoginForm

# Create your views here.
class HomeView(TemplateView):
    template_name = 'main/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["UserLoginForm"] = UserLoginForm()
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            print('AUTHENTICATED')
            try:
                if(self.request.user.doctor):
                    return redirect('doctor:dashboard')
            except:
                pass
            try:
                if(self.request.user.patient):
                    return redirect('patient:dashboard')
            except:
                pass
        return super().get(*args, **kwargs)


