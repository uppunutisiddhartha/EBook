# base/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  Book, Feedback
from django import forms
from .models import LecturerApplication


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'image', 'category', 'selected_item', 'pdf']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter book description'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'selected_item': forms.Select(attrs={'class': 'form-control'}),
            'pdf': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }



# forms.py



class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1)


# forms.py



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    complaint = forms.CharField(widget=forms.Textarea, required=True)






from django import forms


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'rating', 'comments']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comments': forms.Textarea(attrs={'rows': 4}),
        }




# base/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, label='Phone Number')
    address = forms.CharField(widget=forms.Textarea, required=True, label='Address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Save UserProfile fields
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address']
            )
        return user


class SupportRequestForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}), required=True)



# forms.py



# forms.py

from django import forms
from .models import LecturerApplication

class LecturerApplicationForm(forms.ModelForm):
    preferred_subjects = forms.MultipleChoiceField(
        choices=[
            ('M1(Btech)', 'M1(Btech)'), 
            ('DataScience', 'DataScience'), 
            ('compailer Design', 'compailer Design'), 
            ('ADE', 'ADE'),
            ('SPPM', 'SPPM'),
            ('DAA', 'DAA'),
            ('DS', 'DS'),
            ('STM', 'STM'),
            ('M2', 'M2'),
            ('COSM', 'COSM'),
            ('COA', 'COA'),
            ('SE', 'SE'),
            ('BEE', 'BEE'),
            ('Cemistry', 'Cemistry'),
            ('Physics', 'Physics'),
            ('PPS', 'PPS'),
            ('M2', 'M2'),
            # Add more subjects here
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    languages = forms.MultipleChoiceField(
        choices=[
            ('English', 'English'), 
            ('Hindi', 'Hindi'), 
            ('Telugu', 'Telugu'),
            # Add more languages as needed
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = LecturerApplication
        fields = [
            'first_name', 'second_name', 'email', 'phone', 
            'degree_certificate', 'qualification', 'preferred_subjects',
            'languages', 'id_proof', 'profile_pic', 'preferred_time',
            'preferred_days', 'expertise', 'availability', 'experience'
        ]
        widgets = {
            'preferred_time': forms.TextInput(attrs={'placeholder': 'e.g., 10am - 12pm'}),
            'preferred_days': forms.TextInput(attrs={'placeholder': 'e.g., Monday, Wednesday, Friday'}),
        }
