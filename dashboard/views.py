from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from authentication.models import CustomerProfile, NutritionistProfile
from nutritional_plans.models import NutritionalPlan


def dashboard(request):

    if request.user.is_authenticated:
        nutri_profile = NutritionistProfile.objects.filter(
            user=request.user
        ).first()

        if nutri_profile:
            customers = CustomerProfile.objects.filter(
                nutritionist=nutri_profile
            )

            paginator = Paginator(customers, 3)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            context = {
                'customers': page_obj,
                'nutri_profile': nutri_profile
            }

            return render(
                request,
                'dashboard/nutritionist_dashboard.html', context

            )

        customer_profile = CustomerProfile.objects.filter(
            user=request.user
        ).first()

        if customer_profile:
            nutritionist = customer_profile.nutritionist

            nutritional_plans = NutritionalPlan.objects.filter(
                client=request.user
            )

            available_nutritionists = NutritionistProfile.objects.exclude(
                user__customerprofile__isnull=False
            )

            paginator = Paginator(available_nutritionists, 3)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            return render(
                request,
                'dashboard/customer_dashboard.html',
                {
                    'nutritionist': nutritionist,
                    'nutritional_plans': nutritional_plans,
                    'available_nutritionists': page_obj,
                }
            )

    messages.error(request, 'You are not authorized to access this page')
    return redirect('login_create')


@login_required
def select_nutritionist(request, nutritionist_id):
    user = request.user
    customer_profile = CustomerProfile.objects.filter(user=user).first()

    if not customer_profile:
        messages.error(request, "You don't have a customer profile.")
        return redirect('dashboard')

    try:
        nutritionist = NutritionistProfile.objects.get(id=nutritionist_id)
        customer_profile.nutritionist = nutritionist
        customer_profile.save()
        messages.success(
            request, "You have successfully selected a nutritionist."
        )
    except NutritionistProfile.DoesNotExist:
        messages.error(request, "Selected nutritionist does not exist.")

    return redirect('dashboard')
