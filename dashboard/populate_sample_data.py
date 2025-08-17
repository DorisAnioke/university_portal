from django.contrib.auth.models import User
from dashboard.models import Course, Enrollment, Grade, Transaction, LibraryItem, Event, FAQ, Profile
from datetime import date
import random

# ===== Create test students =====
students_data = [
    {'username': 'JohnDoe', 'email': 'johndoe@example.com'},
    {'username': 'JaneSmith', 'email': 'janesmith@example.com'},
    {'username': 'AliceBrown', 'email': 'alicebrown@example.com'},
    {'username': 'BobJohnson', 'email': 'bobjohnson@example.com'},
]

students = []
for s in students_data:
    user, created = User.objects.get_or_create(username=s['username'], email=s['email'])
    if created:
        user.set_password('password123')
        user.save()
    students.append(user)

# ===== Courses =====
courses_data = [
    {'code': 'CSC101', 'name': 'Introduction to Computer Science', 'description': 'Learn basic programming concepts and problem-solving.'},
    {'code': 'MTH101', 'name': 'Calculus I', 'description': 'Introduction to derivatives, integrals, and limits.'},
    {'code': 'PHY101', 'name': 'Physics I', 'description': 'Mechanics, motion, and forces.'},
    {'code': 'ENG101', 'name': 'English Composition', 'description': 'Improve your academic writing skills.'},
    {'code': 'HIS101', 'name': 'World History', 'description': 'Explore major events and civilizations.'},
]

courses = []
for c in courses_data:
    course, created = Course.objects.get_or_create(code=c['code'], name=c['name'], description=c['description'])
    courses.append(course)

# ===== Enrollments & Grades =====
grade_choices = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']

for student in students:
    # Each student randomly enrolls in 3-5 courses
    enrolled_courses = random.sample(courses, k=random.randint(3, 5))
    for course in enrolled_courses:
        enrollment, _ = Enrollment.objects.get_or_create(student=student, course=course)
        # Assign a random grade
        Grade.objects.get_or_create(student=student, course=course, grade=random.choice(grade_choices))

# ===== Transactions =====
transaction_descriptions = [
    ('Tuition Fee Payment', True, 5000),
    ('Lab Fee Payment', True, 300),
    ('Library Fine', False, 100),
    ('Printing Charges', False, 50),
]

for student in students:
    for desc, is_credit, amount in transaction_descriptions:
        # Randomly assign some transactions
        if random.choice([True, False]):
            Transaction.objects.get_or_create(student=student, description=desc, amount=amount, is_credit=is_credit)

# ===== Library Items =====
library_items_data = [
    {'title': 'Data Structures Textbook', 'author': 'John Doe', 'description': 'Comprehensive guide to data structures with exercises.'},
    {'title': 'Calculus Guide', 'author': 'Jane Smith', 'description': 'Step-by-step calculus explanations with examples.'},
    {'title': 'Physics Fundamentals', 'author': 'Albert Newton', 'description': 'Explore classical mechanics with illustrations.'},
    {'title': 'Academic Writing Handbook', 'author': 'Mary Johnson', 'description': 'Tips and rules for effective academic writing.'},
]

for l in library_items_data:
    LibraryItem.objects.get_or_create(title=l['title'], author=l['author'], description=l['description'])

# ===== Events =====
events_data = [
    {'title': 'Freshers Orientation', 'date': date(2025, 9, 1), 'location': 'Main Auditorium', 'description': 'Welcome new students and introduce faculty.'},
    {'title': 'Career Fair', 'date': date(2025, 10, 15), 'location': 'Exhibition Hall', 'description': 'Meet potential employers and internships.'},
    {'title': 'Guest Lecture: AI Trends', 'date': date(2025, 11, 5), 'location': 'Room 204', 'description': 'Learn about AI applications from industry experts.'},
]

for e in events_data:
    Event.objects.get_or_create(title=e['title'], date=e['date'], location=e['location'], description=e['description'])

# ===== FAQs =====
faq_data = [
    {'question': 'How do I reset my password?', 'answer': 'Go to Profile > Change Password and follow instructions.', 'order': 1, 'category': 'Account'},
    {'question': 'How do I enroll in a course?', 'answer': 'Go to Courses page and click Enroll next to the course.', 'order': 2, 'category': 'Courses'},
    {'question': 'How can I check my grades?', 'answer': 'Visit the Grades page to see all your results.', 'order': 3, 'category': 'Grades'},
    {'question': 'Where can I find library resources?', 'answer': 'Go to the Library section to browse or download materials.', 'order': 4, 'category': 'Library'},
    {'question': 'Who do I contact for finance inquiries?', 'answer': 'Email finance@willowheights.edu for support.', 'order': 5, 'category': 'Finance'},
]

for f in faq_data:
    FAQ.objects.get_or_create(question=f['question'], answer=f['answer'], order=f['order'], category=f['category'])

# ===== Profiles =====
for student in students:
    profile, _ = Profile.objects.get_or_create(user=student)
    profile.phone_number = '+2348001234567'
    profile.address = f'{student.username} is a dedicated student in Willow Heights University.'
    profile.bio = 'Passionate about learning and participating in campus activities.'
    profile.save()

print("Multiple students with realistic enrollments, grades, transactions, and profiles populated!")