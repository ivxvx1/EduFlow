from django.contrib import admin
from .models import Review, Course, Unit, Assessment
from .models import Task 


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('topic', 'message', 'created_at')
    
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Assessment)
admin.site.register(Task)


