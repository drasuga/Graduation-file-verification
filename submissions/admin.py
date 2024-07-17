from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models import Q
from .models import Student, Submission

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id')
    search_fields = ('user__username', 'student_id')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'timestamp', 'is_verified', 'certificates_available')
    list_filter = ('is_verified', 'certificates_available', 'timestamp')
    search_fields = ('student__user__username', 'student__student_id')
    actions = ['mark_as_verified', 'mark_as_unverified']
    change_list_template = 'admin/submission_change_list.html'

    def mark_as_verified(self, request, queryset):
        queryset.update(is_verified=True)
    mark_as_verified.short_description = "Mark selected submissions as verified"

    def mark_as_unverified(self, request, queryset):
        queryset.update(is_verified=False)
    mark_as_unverified.short_description = "Mark selected submissions as unverified"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total': Count('id'),
            'verified': Count('id', filter=Q(is_verified=True)),
            'certificates_available': Count('id', filter=Q(certificates_available=True)),
        }
        
        response.context_data['summary'] = list(
            qs.aggregate(**metrics).items()
        )
        
        response.context_data['summary_over_time'] = list(
            qs.annotate(x=TruncDate('timestamp'))
              .values('x')
              .annotate(**metrics)
              .order_by('-x')
        )
        
        return response