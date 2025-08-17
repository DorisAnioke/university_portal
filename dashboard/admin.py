from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.safestring import mark_safe
from .models import HomePage, PortalPage, Course, Enrollment, Grade, Transaction, LibraryItem, Event, Profile, FAQ
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# ===== Inline Admins for User =====
class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    readonly_fields = ('date_enrolled',)
    autocomplete_fields = ('course',)

class GradeInline(admin.TabularInline):
    model = Grade
    extra = 0
    autocomplete_fields = ('course',)

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ('date',)

# ===== Custom User Admin =====
class UserAdmin(DefaultUserAdmin):
    inlines = [EnrollmentInline, GradeInline, TransactionInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

# Unregister default User and register custom UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# ===== HomePage Admin =====
@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'preview_background')
    search_fields = ('title', 'subtitle', 'welcome_message')
    readonly_fields = ('preview_background',)

    def preview_background(self, obj):
        if obj.background_image:
            return mark_safe(f'<img src="{obj.background_image.url}" style="max-height:100px;">')
        return "No image"
    preview_background.short_description = "Background Preview"

# ===== PortalPage Admin =====
@admin.register(PortalPage)
class PortalPageAdmin(admin.ModelAdmin):
    list_display = ('page_key', 'heading')
    search_fields = (
        'heading', 'main_content', 'courses_content', 'grades_content',
        'finance_content', 'library_content', 'events_content',
        'help_content', 'profile_content'
    )

# ===== Course Admin =====
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ('code',)

# ===== Enrollment Admin =====
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')
    list_filter = ('course',)
    search_fields = ('student__username', 'course__name')
    readonly_fields = ('date_enrolled',)
    autocomplete_fields = ('student', 'course')

# ===== Grade Admin =====
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade')
    list_filter = ('course', 'grade')
    search_fields = ('student__username', 'course__name', 'grade')
    autocomplete_fields = ('student', 'course')

# ===== Transaction Admin =====
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('student', 'description', 'amount', 'is_credit', 'date')
    list_filter = ('is_credit', 'date')
    search_fields = ('student__username', 'description')
    readonly_fields = ('date',)
    autocomplete_fields = ('student',)

@admin.register(LibraryItem)
class LibraryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_added')
    search_fields = ('title', 'author', 'description')
    list_filter = ('date_added',)
    
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'description', 'location')
    list_filter = ('date',)
    
    
# Inline Profile inside User admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    readonly_fields = ('profile_picture_preview',)

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" style="max-height:80px; border-radius:50%;">')
        return "No image"
    profile_picture_preview.short_description = "Profile Picture"

# Extend UserAdmin and attach ProfileInline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Unregister the default User admin, register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

    

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'profile_picture_preview')
    search_fields = ('user_username', 'user_email', 'phone', 'address')
    readonly_fields = ('profile_picture_preview',)

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" style="max-height:50px; border-radius:50%;">')
        return "No image"
    profile_picture_preview.short_description = "Profile Picture"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    search_fields = ('question', 'answer')
    