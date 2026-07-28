from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Course, Unit, Assessment, Review, Task
from .forms import CourseForm, UnitForm, AssessmentForm, ReviewForm, TaskForm
from django.urls import reverse
import json

# ==================== 1. HOME PAGE VIEW ======================
def index(request): 
    return render(request, 'index.html')

# ==================== 3. ABOUT VIEW ======================
def about(request):
    return render(request, 'about.html')

# ==================== 4. REVIEWS VIEW (Feedback CRUD) ======================
@login_required
def reviews(request):
    """View to handle submitting and displaying user reviews/feedback."""
    if request.method == "POST":
        if 'send_review' in request.POST:
            # --- Handle Review Submission ---
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your message was sent successfully.")
                return redirect('reviews')
            else:
                messages.error(request, "Error sending message.")

        if 'delete_review_id' in request.POST:
            # --- Handle Review Deletion ---
            review_id = request.POST.get('delete_review_id')
            review = get_object_or_404(Review, pk=review_id)
            review.delete()
            messages.success(request, "Review deleted.")
            return redirect('reviews')

    form = ReviewForm()
    all_reviews = Review.objects.all().order_by('-created_at')
    
    context = {
        'form': form, 
        'reviews': all_reviews
    }
    return render(request, 'reviews.html', context)

# ==================== 5. LIBRARY  ======================
def library(request):
    return render(request, 'library.html')

# ==================== 6. USER LOGIN VIEW ======================
def user_login(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # --- Check user role ---
            if role == 'leader':
                auth_login(request, user) 
                messages.success(request, f"Welcome back, Programme Leader .")
                return redirect('dashboard') 
            else:
                messages.error(request, 'Access Denied: Only Programme Leaders are allowed at this time.')
                return render(request, 'login.html') 
        else:
            
            messages.error(request, 'Invalid Username or Password.')
            return render(request, 'login.html')
            
    return render(request, 'login.html')

# ==================== 7. LOGOUT VIEW ======================
@login_required
def logout(request):
    auth_logout(request)
    return render(request, 'logout.html')

# ==================== 8. CALENDAR VIEW  ======================
@login_required
def Calendar(request):
    if request.method == 'POST':
        if 'add_task' in request.POST:
            # --- Handle Add Task ---
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                messages.success(request, "Task added successfully!")
            else:
                messages.error(request, "Error adding task.")
            return redirect('Calendar')

        if 'delete_task_id' in request.POST:
            # --- Handle Delete Task ---
            task_id = request.POST.get('delete_task_id')
            task = get_object_or_404(Task, pk=task_id) 
            task.delete()
            messages.success(request, "Task deleted successfully.")
            return redirect('Calendar')

    task_form = TaskForm()
    all_tasks = Task.objects.all().order_by('date')
    
    events_data = []
    for task in all_tasks:
        
        color = '#64ADB1'
        if task.user == request.user:
            color = '#e8a649'
            
        events_data.append({
            'id': task.id,
            'title': f"{task.title} (By: {task.user.username if task.user else 'Anon'})", 
            'start': task.date.isoformat(), 
            'color': color,
        })

    context = {
        'tasks': all_tasks,
        'task_form': task_form,
        'events_json': json.dumps(events_data) 
    }
    
    return render(request, 'Calendar.html', context)

# ==================== 9. DASHBOARD VIEW (CRUD) ======================
@login_required
def dashboard(request):

    # 1. Create new course
    if request.method == 'POST' and 'create_course' in request.POST:
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.title}" successfully created.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Error creating course.')

    # 2. Edit course
    if request.method == 'POST' and 'edit_course' in request.POST:
        cid = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=cid)
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.title}" updated successfully.')
            return redirect(f"{reverse('dashboard')}?manage={cid}")

    # 3. DELETE COURSE 
    if request.method == 'POST' and 'delete_course_id' in request.POST:
        cid = request.POST.get('delete_course_id')
        course_qs = Course.objects.filter(pk=cid)
        if course_qs.exists():
            course_qs.delete()
            messages.success(request, 'Course deleted successfully.')
        return redirect('dashboard')

    # 4. Add Unit
    if request.method == 'POST' and 'add_unit' in request.POST:
        uid_course = request.POST.get('unit_course')
        course = get_object_or_404(Course, pk=uid_course)
        uf = UnitForm(request.POST, request.FILES)
        if uf.is_valid():
            unit = uf.save(commit=False)
            unit.course = course
            unit.save()
            messages.success(request, f'Unit "{unit.title}" added.')
            return redirect(f"{reverse('dashboard')}?manage={course.id}")

    # 5. Edit Unit
    if request.method == 'POST' and 'edit_unit' in request.POST:
        uid = request.POST.get('unit_id')
        course_id = request.POST.get('unit_course')
        unit = get_object_or_404(Unit, pk=uid)
        form = UnitForm(request.POST, request.FILES, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Unit "{unit.title}" updated successfully.')
            return redirect(f"{reverse('dashboard')}?manage={course_id}")
        else:
            messages.error(request, 'Error updating unit.')

    # 6. DELETE UNIT 
    if request.method == 'POST' and 'delete_unit_id' in request.POST:
        uid = request.POST.get('delete_unit_id')
        course_id = request.POST.get('unit_course')
        unit_qs = Unit.objects.filter(pk=uid)
        if unit_qs.exists():
            unit_qs.delete()
            messages.success(request, 'Unit deleted successfully.')
        return redirect(f"{reverse('dashboard')}?manage={course_id or ''}")

    # 7. Add Assessment
    if request.method == 'POST' and 'add_assessment' in request.POST:
        ac_course = request.POST.get('assessment_course')
        course = get_object_or_404(Course, pk=ac_course)
        af = AssessmentForm(request.POST, request.FILES)
        if af.is_valid():
            assessment = af.save(commit=False)
            assessment.course = course
            assessment.save()
            messages.success(request, f'Assessment "{assessment.title}" added.')
            return redirect(f"{reverse('dashboard')}?manage={course.id}")

    # 8. Edit Assessment
    if request.method == 'POST' and 'edit_assessment' in request.POST:
        aid = request.POST.get('assessment_id')
        course_id = request.POST.get('assessment_course')
        assessment = get_object_or_404(Assessment, pk=aid)
        form = AssessmentForm(request.POST, request.FILES, instance=assessment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Assessment "{assessment.title}" updated successfully.')
            return redirect(f"{reverse('dashboard')}?manage={course_id}")
        else:
            messages.error(request, 'Error updating assessment.')

    # 9. DELETE ASSESSMENT (DIRECT)
    if request.method == 'POST' and 'delete_assessment_id' in request.POST:
        aid = request.POST.get('delete_assessment_id')
        course_id = request.POST.get('assessment_course')
        assessment_qs = Assessment.objects.filter(pk=aid)
        if assessment_qs.exists():
            assessment_qs.delete()
            messages.success(request, 'Assessment deleted successfully.')
        return redirect(f"{reverse('dashboard')}?manage={course_id or ''}")


    

    # --- Fetch and order all courses ---
    courses = Course.objects.all().order_by('-created_at')
    
   
    search_query = request.GET.get('q')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(leader_of_course__icontains=search_query)
        ).distinct()

    create_form = CourseForm()
    unit_form = UnitForm()
    assessment_form = AssessmentForm()

    manage_id = request.GET.get('manage')
    manage_course = None
    units = None
    assessments = None
    edit_course_form = None
    
    
    edit_unit_form = None
    edit_unit_id = request.GET.get('edit_unit')
    
    edit_assessment_form = None
    edit_assessment_id = request.GET.get('edit_assessment')

    if manage_id:
        manage_course = get_object_or_404(Course, pk=manage_id)
        units = manage_course.units.all().order_by('-created_at')
        assessments = manage_course.assessments.all().order_by('-created_at')
        edit_course_form = CourseForm(instance=manage_course)

        if edit_unit_id:
            try:
                unit_instance = Unit.objects.get(pk=edit_unit_id)
                edit_unit_form = UnitForm(instance=unit_instance)
            except Unit.DoesNotExist:
                pass

        if edit_assessment_id:
            try:
                assessment_instance = Assessment.objects.get(pk=edit_assessment_id)
                edit_assessment_form = AssessmentForm(instance=assessment_instance)
            except Assessment.DoesNotExist:
                pass
        
    context = {
        'courses': courses,
        'create_form': create_form,
        'manage_course': manage_course,
        'units': units,
        'assessments': assessments,
        'unit_form': unit_form,
        'assessment_form': assessment_form,
        'edit_course_form': edit_course_form,
        
        'edit_unit_form': edit_unit_form,
        'edit_unit_id': edit_unit_id,
        'edit_assessment_form': edit_assessment_form,
        'edit_assessment_id': edit_assessment_id,
    }
    return render(request, 'dashboard.html', context)


@login_required
def courses_table(request):
    all_courses = Course.objects.all().order_by('id')
    return render(request, 'courses_table.html', {
        'courses': all_courses
    })

@login_required
def course_report(request):

    courses_stats = Course.objects.annotate(
        total_units=Count('units', distinct=True),
        total_assessments=Count('assessments', distinct=True)
    ).order_by('id')
    
    return render(request, 'course_report.html', {
        'courses': courses_stats
    })