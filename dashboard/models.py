from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField  
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver


class PortalPage(models.Model):
    PAGE_CHOICES = [
        ('dashboard', 'Dashboard'),
        ('courses', 'Courses'),
        ('grades', 'Grades'),
        ('profile', 'Profile'),
        ('finance', 'Finance'),
        ('library', 'Library'),
        ('events', 'Events'),
        ('help', 'Help'),
    ]

    page_key = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    heading = models.CharField(max_length=200)

    # Main page content
    main_content = HTMLField(blank=True, null=True)

    # Section-specific rich text fields
    courses_content = HTMLField(blank=True, null=True)
    grades_content = HTMLField(blank=True, null=True)
    finance_content = HTMLField(blank=True, null=True)
    library_content = HTMLField(blank=True, null=True)
    events_content = HTMLField(blank=True, null=True)
    help_content = HTMLField(blank=True, null=True)
    profile_content = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.heading

    def get_active_content(self):
        """Return the correct content for this page based on page_key."""
        mapping = {
            'dashboard': self.main_content,
            'courses': self.courses_content,
            'grades': self.grades_content,
            'finance': self.finance_content,
            'library': self.library_content,
            'events': self.events_content,
            'help': self.help_content,
            'profile': self.profile_content,
        }
        content = mapping.get(self.page_key, self.main_content)
        return content if content else "<p><em>Content coming soon...</em></p>"

class HomePage(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    welcome_message = HTMLField(blank=True)  # Rich text for welcome message
    background_image = models.ImageField(upload_to='homepage/')  # Keep homepage background

    def __str__(self):
        return self.title

class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    description = HTMLField(blank=True)  # Rich text for course description

    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.username} - {self.course.code}: {self.grade}"

class Transaction(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    is_credit = models.BooleanField(default=False)  # True = Payment received, False = Fee

    def __str__(self):
        return f"{self.student.username} - {self.description} ({'Credit' if self.is_credit else 'Debit'})"
    
class LibraryItem(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    description = HTMLField(blank=True)
    pdf_file = models.FileField(upload_to='library_pdfs/', blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('sports', 'Sports'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = HTMLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return self.title
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def image_tag(self):
        if self.profile_picture:
            return mark_safe(f'<img src="{self.profile_picture.url}" style="height:50px;"/>')
        return "No Image"
    image_tag.short_description = "Profile Picture"

# ===== Signals to create/update Profile automatically =====
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('admissions', 'Admissions'),
        ('finance', 'Finance'),
        ('courses', 'Courses'),
        ('technical', 'Technical'),
        ('other', 'Other'),
    ]
    question = models.CharField(max_length=300)
    answer = HTMLField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return self.question
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', default='profile_pics/default.png', blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"