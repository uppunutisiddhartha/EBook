from django.contrib import admin
from .models import  Book,Note,CartItem,Feedback,SupportRequest, LecturerApplication, ClassRequest


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'category')
    search_fields = ('title', 'author', 'description')
    readonly_fields = ('approval_token', 'created_at', 'updated_at')
    actions = ['approve_selected_books', 'reject_selected_books']

    def approve_selected_books(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected books have been approved.")
    approve_selected_books.short_description = "Approve selected books"

    def reject_selected_books(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected books have been rejected and deleted.")
    reject_selected_books.short_description = "Reject selected books"


    
admin.site.register(Note)



# your_app/admin.py
"""
from django.contrib import admin
from .models imp
ort Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at')
    search_fields = ('text',)
  """
  
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Inline admin to show UserProfile fields within User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False  # Prevent deletion from user admin
    verbose_name_plural = 'Profile'
    fields = ('phone_number', 'address')  # Fields to display in the user edit page

# Extend User admin to include the inline profile fields
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)  # Attach the profile fields to the User admin

# Unregister the default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)



#cART
@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "quantity", "added_at"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass
    
    
@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'created_at', 'status')
    list_filter = ('status',)
    
    
    
import random
from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import LecturerApplication

from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random

class LecturerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'email', 'qualification', 'experience', 'application_status')

    def generate_password(self, last_name, phone):
        # Construct password from last name and last 3 digits of mobile number
        return f"{last_name.lower()}@{str(phone)[-3:]}"

    def generate_username(self, first_name, last_name):
        # Combine names and add two random digits
        return f"{first_name.lower()}.{last_name.lower()}@{random.randint(10, 99)}"

    def save_model(self, request, obj, form, change):
        # Handle approved application
        if obj.application_status == 'Approved' and not obj.user:
            username = self.generate_username(obj.first_name, obj.second_name)
            password = self.generate_password(obj.second_name, obj.phone)

            # Create user with generated username and password
            user = User.objects.create_user(username=username, email=obj.email, password=password)

            # Link the user to the LecturerApplication model
            obj.user = user
            obj.is_lecturer = True
            obj.save()

            # Send approval email
            send_mail(
                'Your Application has been Approved',
                f'Congratulations {obj.first_name}, your application has been approved. '
                f'Your login credentials are:\n\nUser ID: {username}\nPassword: {password}',
                settings.EMAIL_HOST_USER,
                [obj.email],
                fail_silently=False,
            )

        # Handle rejected application
        elif obj.application_status == 'Rejected':
            # Get rejection reason or default to "No reason provided"
            rejection_reason = obj.rejection_reason if obj.rejection_reason else "No reason provided."

            # Send rejection email
            send_mail(
                'Your Application has been Rejected',
                f'Dear {obj.first_name},\n\nThank you for applying. Unfortunately, your application was not approved.\n\n'
                f'Reason: {rejection_reason}',
                settings.EMAIL_HOST_USER,
                [obj.email],
                fail_silently=False,
            )

        # Call the super method to save the model
        super().save_model(request, obj, form, change)

# Register the model with the custom admin
admin.site.register(LecturerApplication, LecturerAdmin)

@admin.register(ClassRequest)
class ClassRequestAdmin(admin.ModelAdmin):
    list_display = ('topic', 'category', 'status', 'time')
    list_filter = ('category', 'status')
    search_fields = ('topic', 'user__username')


