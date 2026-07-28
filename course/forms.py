from django import forms
from .models import Course, Unit, Assessment
from .models import Review
from .models import Task

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'leader_of_course', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Course Title','required':True}),
            'leader_of_course': forms.TextInput(attrs={'placeholder':'Enter the name of the leader','required':True}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Unit Title','required':True}),
            'description': forms.Textarea(attrs={'placeholder':'Unit Description (Optional)','rows':2}),
        }

class AssessmentForm(forms.ModelForm):
    deadline = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = Assessment
        fields = ['title', 'description', 'file', 'grade', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Assessment Title','required':True}),
            'description': forms.Textarea(attrs={'placeholder':'Description (Optional)','rows':2}),
            'grade': forms.TextInput(attrs={'placeholder':'Maximum Grade (e.g., 100)'}),
        }
        


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['topic', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your message here...'}),
            'topic': forms.TextInput(attrs={'placeholder': 'Topic (optional)'}),
        }



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "date"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }