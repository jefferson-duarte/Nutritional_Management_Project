from django.contrib import messages
from django.shortcuts import redirect, render

from authentication.models import CustomerProfile, NutritionistProfile


def dashboard(request):

    if request.user.is_authenticated:
        nutri_profile = NutritionistProfile.objects.filter(
            user=request.user
        ).first()

        if nutri_profile:
            customers = CustomerProfile.objects.filter(
                nutritionist=nutri_profile
            )
            return render(
                request,
                'dashboard/nutritionist_dashboard.html',
                {'customers': customers}
            )

        customer_profile = CustomerProfile.objects.filter(
            user=request.user
        ).first()
        if customer_profile:
            nutritionist = customer_profile.nutritionist
            return render(
                request,
                'dashboard/customer_dashboard.html',
                {'nutritionist': nutritionist}
            )

    messages.error(request, 'You are not authorized to access this page')
    return redirect('login_create')
