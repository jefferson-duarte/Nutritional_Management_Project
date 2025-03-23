from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NutritionalPlanForm
from .models import NutritionalPlan


@login_required
def nutritional_plan_list(request):
    plans = NutritionalPlan.objects.filter(nutritionist=request.user)
    return render(request, 'nutritional_plans/plan_list.html', {'plans': plans})  # noqa:E501


@login_required
def nutritional_plan_create(request):
    if request.method == 'POST':
        form = NutritionalPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.nutritionist = request.user
            plan.save()
            return redirect('plan_list')
    else:
        form = NutritionalPlanForm()
    return render(request, 'nutritional_plans/plan_form.html', {'form': form})


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
