# models.py

from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_lecturer = models.BooleanField(default=False)  # Add this field
    

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('library', 'E.Library'),
        ('BTech', 'B.Tech'),
        ('MBA', 'MBA'),
        ('MCA', 'MCA'),
        ('Degree', 'Degree'),
    ]

    title = models.CharField(max_length=255, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='uploads/books/covers/', blank=True, null=True)
    rating = models.IntegerField(default=0)
    pdf = models.FileField(upload_to='books/pdfs/', null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE) 
    views = models.PositiveIntegerField(default=0) 
    
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default="library", null=False, blank=False)
    selected_item = models.CharField(max_length=100, default="history", null=True, blank=True)
    
    # New Fields for Approval Workflow
    is_approved = models.BooleanField(default=False)
    approval_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True) 
    views = models.PositiveIntegerField(default=0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title
    
    
    
#cart


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use correct field
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Use correct field
    quantity = models.IntegerField(default=1)
    added_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    
    
    
    


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)  
    email = models.EmailField() 
    rating = models.PositiveIntegerField(default=1)  
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}"

    



class SupportRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject



from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return self.user.username






from django.db import models
from django.contrib.auth.models import User

class ClassRequest(models.Model):
    CATEGORY_CHOICES = [
        ('Math', 'Mathematics'),
        ('Science', 'Science'),
        # Add more categories as needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    topic = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Accepted, Rejected
    rejection_reason = models.TextField(null=True, blank=True)
    zoom_link = models.URLField(null=True, blank=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.topic} ({self.category}) - {self.status}"












from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes')  # Made non-nullable
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book_note')
        ]
        ordering = ['-updated_at']

    def __str__(self):
        return f"Note by {self.user.username} on {self.book.title}"
    



from django.db import models

class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=50) 
    zoom_link = models.URLField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.name


from django.db import models

class LecturerApplication(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    degree_certificate = models.FileField(upload_to='certificates/')
    qualification = models.CharField(max_length=100)
    preferred_subjects = models.CharField(max_length=200)
    languages = models.CharField(max_length=200)
    id_proof = models.FileField(upload_to='id_proof/')
    profile_pic = models.ImageField(upload_to='profile_pics/')
    preferred_time = models.CharField(max_length=100)
    preferred_days = models.CharField(max_length=100)
    expertise = models.CharField(max_length=200)
    availability = models.CharField(max_length=100)
    experience = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    zoom_link = models.URLField(max_length=500, blank=True, null=True) 
    rejection_reason = models.TextField(blank=True, null=True) 
    is_lecturer = models.BooleanField(default=False) 
    # New field for rejection reason
    application_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    

from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

