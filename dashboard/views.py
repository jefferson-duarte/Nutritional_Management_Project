from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from authentication.models import CustomerProfile, NutritionistProfile
from nutritional_plans.models import NutritionalPlan

from .forms import AppointmentForm
from .models import Appointment


def dashboard(request):

    if request.user.is_authenticated:
        nutri_profile = NutritionistProfile.objects.filter(
            user=request.user
        ).first()

        if nutri_profile:
            customers = CustomerProfile.objects.filter(
                nutritionist=nutri_profile
            )

            last_appointments = {}

            for customer in customers:
                last_appointment = Appointment.objects.filter(customer=customer).order_by('-date').first()  # noqa:E501
                last_appointments[customer.id] = last_appointment

            appointments = Appointment.objects.filter(
                nutritionist=nutri_profile).order_by('date')

            paginator = Paginator(customers, 3)
            page_number = request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)

            context = {
                'customers': page_obj,
                'appointments': appointments,
                'nutri_profile': nutri_profile,
                'last_appointments': last_appointments,
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

            customer_appointments = Appointment.objects.filter(
                customer=customer_profile).order_by('date')

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
                    'appointments': customer_appointments,
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


def schedule_appointment(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in.")
        return redirect("login_create")

    nutritionist_profile = NutritionistProfile.objects.filter(
        user=request.user).first()
    if not nutritionist_profile:
        messages.error(
            request, "Only nutritionists can schedule appointments.")
        return redirect("dashboard")

    customers = CustomerProfile.objects.filter(
        nutritionist=nutritionist_profile  # noqa:E501
    )

    if request.method == "POST":
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.nutritionist = nutritionist_profile
            appointment.save()
            messages.success(request, "Appointment scheduled successfully!")
            return redirect("dashboard")
    else:
        form = AppointmentForm(user=request.user)  # Passa o usuário logado

    context = {
        "form": form,
        "customers": customers,
    }

    return render(request, "appointments/schedule_appointment.html", context)  # noqa:E501


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.nutritionist.user:
        messages.error(request, "You can only cancel your own appointments.")
        return redirect("dashboard")

    appointment.status = "canceled"
    appointment.save()
    messages.success(request, "Appointment canceled successfully.")
    return redirect("dashboard")


def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.nutritionist.user:
        messages.error(
            request, "You can only reschedule your own appointments.")
        return redirect("dashboard")

    customers = CustomerProfile.objects.filter(
        nutritionist=appointment.nutritionist
    )

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment rescheduled successfully!")
            return redirect("dashboard")
    else:
        form = AppointmentForm(instance=appointment)

    context = {
        "form": form,
        "customers": customers,
    }

    return render(request, "appointments/reschedule_appointment.html", context)  # noqa:E501


def confirm_delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.nutritionist.user:
        messages.error(request, "You can only delete your own appointments.")
        return redirect("dashboard")

    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Appointment deleted successfully!")
        return redirect("dashboard")

    return render(request, "appointments/confirm_delete_appointment.html", {
        "appointment": appointment
    })


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.nutritionist.user:
        messages.error(request, "You can only delete your own appointments.")
        return redirect("dashboard")

    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect("dashboard")
