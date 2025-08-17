from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import HomePage, PortalPage, Course, Enrollment, Grade, Transaction, LibraryItem, Event, FAQ

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User  
from django.db.models import Sum, Count
from django.db.models import Q
from .models import Profile
from .forms import ProfileForm  



# Home page view
def home(request):
    home_page = HomePage.objects.first()
    pages = PortalPage.objects.all()
    return render(request, 'dashboard/home.html', {
        'home_page': home_page,
        'pages': pages
    })


@login_required
def portal_page(request, page_key):
    page = get_object_or_404(PortalPage, page_key=page_key)
    context = {'page': page}

    search_query = request.GET.get('search', '')

    if page_key == "courses":
        enrollments = Enrollment.objects.filter(student=request.user)
        if search_query:
            enrollments = enrollments.filter(course__name__icontains=search_query)
        context['enrollments'] = enrollments
        context['search_query'] = search_query

    elif page_key == "grades":
        grades = Grade.objects.filter(student=request.user)
        if search_query:
            grades = grades.filter(course__name__icontains=search_query)
        context['grades'] = grades
        context['search_query'] = search_query

    elif page_key == "library":
        library_items = LibraryItem.objects.all()
        if search_query:
            library_items = library_items.filter(
                Q(title__icontains=search_query) | Q(author__icontains=search_query)
            )
        context['library_items'] = library_items
        context['search_query'] = search_query

    elif page_key == "finance":
        transactions = Transaction.objects.filter(student=request.user)
        if search_query:
            transactions = transactions.filter(description__icontains=search_query)
        context['transactions'] = transactions
        context['search_query'] = search_query

    elif page_key == "events":
        events = Event.objects.all().order_by('date')
        context['events'] = events

    elif page_key == "profile":
        profile, _ = Profile.objects.get_or_create(user=request.user)
        context['profile'] = profile

    elif page_key == "help":
        faqs = FAQ.objects.all()
        context['faqs'] = faqs

    return render(request, 'dashboard/page.html', context)


# Portal landing page view
@login_required
def portal_landing(request):
    pages = PortalPage.objects.all()
    return render(request, 'dashboard/portal_landing.html', {'pages': pages})


# Register new user view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    
    return render(request, 'dashboard/register.html', {'form': form})


@staff_member_required
def admin_dashboard(request):
    # Total counts
    total_students = User.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    total_transactions = Transaction.objects.count()

    # Enrollments per course
    courses = Course.objects.all()
    for course in courses:
        course.enrollment_count = Enrollment.objects.filter(course=course).count()

    # Transaction totals
    total_credit = Transaction.objects.filter(is_credit=True).aggregate(total=Sum('amount'))['total'] or 0
    total_debit = Transaction.objects.filter(is_credit=False).aggregate(total=Sum('amount'))['total'] or 0

    # Grades distribution
    grade_distribution = Grade.objects.values('grade').annotate(count=Count('grade'))
    grade_labels = [item['grade'] for item in grade_distribution]
    grade_counts = [item['count'] for item in grade_distribution]

    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_transactions': total_transactions,
        'courses': courses,
        'total_credit': total_credit,
        'total_debit': total_debit,
        'grade_labels': grade_labels,
        'grade_counts': grade_counts,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)



@login_required
def portal_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    search_query = request.GET.get('search', '')  

    if search_query:
        enrollments = enrollments.filter(
            Q(course__name__icontains=search_query) |
            Q(course__code__icontains=search_query)
        )

    context = {
        'enrollments': enrollments,
        'search_query': search_query,
    }
    return render(request, 'dashboard/portal_courses.html', context)



@login_required
def portal_grades(request):
    grades = Grade.objects.filter(student=request.user).select_related('course')
    search_query = request.GET.get('search', '')  # Get search input from URL

    if search_query:
        grades = grades.filter(
            Q(course__name__icontains=search_query) |
            Q(course__code__icontains=search_query)
        )

    context = {
        'grades': grades,
        'search_query': search_query,
    }
    return render(request, 'dashboard/portal_grades.html', context)



@login_required
def portal_finance(request):
    transactions = Transaction.objects.filter(student=request.user)
    search_query = request.GET.get('search', '')  # For description search
    type_filter = request.GET.get('type', '')    # For credit/debit filter

    if search_query:
        transactions = transactions.filter(description__icontains=search_query)

    if type_filter == 'credit':
        transactions = transactions.filter(is_credit=True)
    elif type_filter == 'debit':
        transactions = transactions.filter(is_credit=False)

    context = {
        'transactions': transactions,
        'search_query': search_query,
        'type_filter': type_filter,
    }
    return render(request, 'dashboard/portal_finance.html', context)
@login_required
def library_page(request):
    items = LibraryItem.objects.all()
    search_query = request.GET.get('search', '')  # get search input

    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    context = {
        'items': items,
        'search_query': search_query,
    }
    return render(request, 'dashboard/library.html', context)@login_required

@login_required
def events_page(request):
    category_filter = request.GET.get('category', '')
    events = Event.objects.all().order_by('date')

    if category_filter:
        events = events.filter(category=category_filter)

    context = {
        'events': events,
        'category_filter': category_filter,
        'categories': Event.CATEGORY_CHOICES,
    }
    return render(request, 'dashboard/events.html', context)

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'dashboard/profile.html', {'form': form})

@login_required
def help_page(request):
    page = get_object_or_404(PortalPage, page_key='help')
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    faqs = FAQ.objects.all()

    if search_query:
        faqs = faqs.filter(
            Q(question__icontains=search_query) |
            Q(answer__icontains=search_query)
        )
    if category_filter:
        faqs = faqs.filter(category=category_filter)

    context = {
        'page': page,
        'faqs': faqs,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': FAQ.CATEGORY_CHOICES,
    }
    return render(request, 'dashboard/help.html', context)


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard:portal_page', page_key='profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'dashboard/edit_profile.html', {'form': form})