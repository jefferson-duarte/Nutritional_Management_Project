from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from authentication.models import CustomerProfile

from .forms import NutritionalPlanForm
from .models import NutritionalPlan


@login_required
def nutritional_plan_list(request):
    plans = NutritionalPlan.objects.filter(nutritionist=request.user)
    return render(request, 'nutritional_plans/plan_list.html', {'plans': plans})  # noqa:E501


@login_required
def nutritional_plan_create(request, customer_id=None):
    customer = None

    if customer_id:
        customer = get_object_or_404(CustomerProfile, id=customer_id)

        if customer.nutritionist and customer.nutritionist.user != request.user:  # noqa:E501
            return HttpResponseForbidden("You are not authorized to prescribe for this client.")  # noqa:E501

    if request.method == 'POST':
        form = NutritionalPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.nutritionist = request.user
            if customer:
                plan.customer = customer.user
            plan.save()
            return redirect('plan_list')
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
    if request.method == 'POST':
        form = NutritionalPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('plan_list')
    else:
        form = NutritionalPlanForm(instance=plan)
    return render(request, 'nutritional_plans/plan_form.html', {'form': form})


@login_required
def nutritional_plan_detail(request, pk):
    plan = get_object_or_404(NutritionalPlan, pk=pk, nutritionist=request.user)
    return render(request, 'nutritional_plans/plan_detail.html', {'plan': plan})  # noqa:E501


@login_required
def nutritional_plan_delete(request, pk):
    plan = get_object_or_404(NutritionalPlan, pk=pk, nutritionist=request.user)
    if request.method == 'POST':
        plan.delete()
        return redirect('plan_list')
    return render(request, 'nutritional_plans/plan_confirm_delete.html', {'plan': plan})  # noqa:E501
