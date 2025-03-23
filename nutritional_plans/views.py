from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from authentication.models import CustomerProfile

from .forms import NutritionalPlanForm
from .models import NutritionalPlan


@login_required
def nutritional_plan_list(request, customer_id):
    customer = get_object_or_404(CustomerProfile, id=customer_id)

    if customer.nutritionist.user != request.user:
        return HttpResponseForbidden("You are not authorized to view this client's plans.")  # noqa:E501

    plans = NutritionalPlan.objects.filter(client=customer.user)

    context = {
        'customer': customer,
        'plans': plans,
    }
    return render(request, 'nutritional_plans/plan_list.html', context)


@login_required
def nutritional_plan_create(request, customer_id=None):
    customer = None

    if customer_id:
        customer = get_object_or_404(CustomerProfile, id=customer_id)

    if request.method == 'POST':
        form = NutritionalPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.nutritionist = request.user
            if customer:
                plan.client = customer.user
            plan.save()
            return redirect('plan_list', customer.id)
    else:
        form = NutritionalPlanForm()
        if customer:
            form.fields['client'].initial = customer.user

    context = {
        'form': form,
        'customer': customer
    }

    return render(request, 'nutritional_plans/plan_form.html', context)


@login_required
def nutritional_plan_edit(request, pk):
    plan = get_object_or_404(NutritionalPlan, pk=pk, nutritionist=request.user)

    try:
        customer = CustomerProfile.objects.get(user=plan.client)
        customer_id = customer.id
    except CustomerProfile.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = NutritionalPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan_list', customer_id=customer_id)

    else:
        form = NutritionalPlanForm(instance=plan)

    context = {
        'form': form,
        'plan': plan
    }

    return render(request, 'nutritional_plans/plan_form.html', context)


@login_required
def nutritional_plan_detail(request, pk):
    plan = get_object_or_404(NutritionalPlan, pk=pk)
    customer = CustomerProfile.objects.get(user=plan.client)

    context = {
        'plan': plan,
        'customer': customer  # Passa o customer para o template
    }

    return render(request, 'nutritional_plans/plan_detail.html', context)


@login_required
def nutritional_plan_delete(request, pk):
    plan = get_object_or_404(NutritionalPlan, pk=pk, nutritionist=request.user)

    try:
        customer = CustomerProfile.objects.get(user=plan.client)
        customer_id = customer.id
    except CustomerProfile.DoesNotExist:
        messages.error(request, "Customer profile not found.")
        return redirect('dashboard')

    if request.method == 'POST':
        plan.delete()
        return redirect('plan_list', customer_id=customer_id)

    return render(request, 'nutritional_plans/plan_confirm_delete.html', {'plan': plan})  # noqa:E501
