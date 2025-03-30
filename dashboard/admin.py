from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('nutritionist', 'customer', 'date', 'status')
    list_filter = ('status',)
    search_fields = ('nutritionist__user__username',
                     'customer__user__username')
    date_hierarchy = 'date'
    ordering = ('-date',)
    list_per_page = 10
    list_display_links = ('nutritionist', 'customer')
    list_editable = ('status',)
    actions = ['mark_as_completed', 'mark_as_canceled']
