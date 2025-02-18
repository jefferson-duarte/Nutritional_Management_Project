from django.contrib import messages
from django.shortcuts import redirect, render

from authentication.models import CustomerProfile, NutritionistProfile


def dashboard(request):

    if request.user.is_authenticated:
        nutri_profile = NutritionistProfile.objects.filter(user=request.user)
        customer_profile = CustomerProfile.objects.filter(user=request.user)

        if nutri_profile.exists():
            customers = CustomerProfile.objects.all()
            return render(request, 'dashboard/nutritionist_dashboard.html', {'customers': customers})

        elif customer_profile.exists():
            return render(request, 'dashboard/customer_dashboard.html')

    messages.error(request, 'You are not authorized to access this page')
    return redirect('login_create')
