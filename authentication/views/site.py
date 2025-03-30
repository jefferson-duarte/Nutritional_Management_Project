from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from ..forms import CustomerAdditionalInfoForm
from ..models import CustomerProfile, NutritionistProfile


def home(request):
    return render(request, 'authentication/home.html')


def login_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('additional_info')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_create')
    return render(request, 'authentication/login.html')


def register_nutritionist(request):
    return render(request, 'authentication/nutritionist_registration.html')


def register_customer(request):
    return render(request, 'authentication/customer_registration.html')


@login_required
def additional_info(request):
    nutritionist_profile = NutritionistProfile.objects.filter(user=request.user)  # noqa:E501

    if nutritionist_profile.exists():
        return redirect('dashboard')

    try:
        customer_profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        return redirect('register_customer')

    if customer_profile.profile_complete:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomerAdditionalInfoForm(
            request.POST,
            request.FILES,
            instance=customer_profile
        )
        if form.is_valid():
            form.save()
            customer_profile.profile_complete = True
            customer_profile.save()
            return redirect('dashboard')
    else:
        form = CustomerAdditionalInfoForm(instance=customer_profile)

    return render(
        request,
        'authentication/additional_info.html',
        {'form': form}
    )


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomerProfile
    form_class = CustomerAdditionalInfoForm
    template_name = 'authentication/update_customer.html'
    pk_url_kwarg = 'customer_id'

    def get_success_url(self):
        messages.success(self.request, 'Customer updated successfully')
        return reverse_lazy('dashboard')

    def get_queryset(self):
        return CustomerProfile.objects.filter(nutritionist=self.request.user.nutritionistprofile)  # noqa:E501

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.object
        return context


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login_create')
