from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    leader_of_course = models.CharField(max_length=255)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Unit(models.Model):
    course = models.ForeignKey(Course, related_name='units', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='unit_files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

class Assessment(models.Model):
    course = models.ForeignKey(Course, related_name='assessments', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='assessment_files/', blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"



class Review(models.Model):
    topic = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic or 'General Message'} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"



from django.contrib.auth.models import User 
class Task(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return f"{self.title} - {self.date} (By: {self.user.username if self.user else 'Anon'})"
    
    
