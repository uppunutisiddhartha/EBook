from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import  Book
from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from base.models import LecturerApplication
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q  # Make sure to import Q for queries
#from .forms import NoteForm
from .models import Note , CartItem
from datetime import datetime

from .utils import send_notification_email
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import ContactForm
import openai 
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .forms import FeedbackForm
from django.contrib.auth.models import User
from .models import LecturerApplication
import datetime
from django.utils.html import strip_tags
from django.core.mail import send_mail
from datetime import datetime
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q


from openai import OpenAI
import json
import os

import logging
logger = logging.getLogger(__name__)




@login_required
def index(request):
    star_range = range(1, 6)
    search_category = request.GET.get('category', '')
    search_item = request.GET.get('selected_item', '')

    if search_category or search_item:
        data = Book.objects.filter(
            Q(category__icontains=search_category) & 
            Q(selected_item__icontains=search_item) &
            Q(is_approved=True)
        )
    else:
        data = Book.objects.filter(is_approved=True)

    # Get the total book count
    total_books = data.count()

    context = {
        "data": data,
        'star_range': star_range,
        "search_category": search_category,
        "search_item": search_item,
        "total_books": total_books,  # Add the count to context
    }
    return render(request, "index.html", context)
@login_required
def logout_view(request):
    logout(request)
    return redirect('base:login')  

from django.contrib.auth import login

from datetime import datetime  # This imports the datetime class from the datetime module

def authView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            
            # Prepare email content
            current_year = datetime.now().year  # Correct usage of datetime.now()
            html_message = render_to_string('emails/thank_you_email.html', {'current_year': current_year})
            plain_message = strip_tags(html_message)  
            
          

            return redirect('base:login') ,
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})



def view_cart(request):
    return render(request,"view_cart.html")




#def note(request):
   # if re
    
def details(request):
    return render(request, "details.html")

def btech(request):
    return render(request, "btech.html")

def insert_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        description = request.POST.get("description")
        category = request.POST.get('category')
        selected_item = request.POST.get('selected_item')
        image = request.FILES.get("photo")  
        pdf_file = request.FILES.get("pdfFile")  
        email = request.POST.get("email")  # Capture the email from form

        book = Book(
            title=title,
            author=author,
            description=description,
            image=image,
            category=category,
            selected_item=selected_item,
            pdf=pdf_file,
            submitted_by=request.user ,
            is_approved=False  # Initially not approved
        )
        book.save()
        subject = "Book Submission Confirmation"
        message = (
   
    f"Dear {request.user.username},\n\n"
    f"Thank you for submitting your book, '{title}', to the E.Book Community! "
    "We are truly grateful for your contribution, and your efforts mean a lot to us.\n\n"
    "Our team will carefully review your submission to ensure it aligns with our guidelines. "
    "We’ll notify you as soon as the approval process is complete.\n\n"
    "If you have any questions or need further assistance, don't hesitate to reach out. "
    "We're always here to help and value your involvement in making this community better.\n\n"
    "With sincere appreciation,\n"
    "The E.Book Community Team"
)
   
              
                 
 

        send_notification_email(request.user.email, subject, message)
        # Sending confirmation email to the user
        subject = "Book Submission Confirmation"
        
        html_content = render_to_string('emails/submission_confirmation.html', {
            'title': title,
            'author': author,
        })
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=f"Hi,\n\nThank you for submitting your book '{title}' by {author}. It is currently pending approval.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email_message.attach_alternative(html_content, "text/html")
        email_message.send(fail_silently=False)

        # Proceed to send admin email with approval links as before
        approval_link = request.build_absolute_uri(
            reverse('base:approve_book', args=[book.approval_token])
        )
        rejection_link = request.build_absolute_uri(
            reverse('base:reject_book', args=[book.approval_token])
        )
        
        subject = f"New Book Submission: {book.title}"
        html_content = render_to_string('emails/approval_email.html', {
            'book': book,
            'approval_link': approval_link,
            'rejection_link': rejection_link,
        })
        text_content = render_to_string('emails/approval_email.txt', {
            'book': book,
            'approval_link': approval_link,
            'rejection_link': rejection_link,
        })

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

        return render(request, "addbook.html", {"message": "Book submitted successfully and is pending admin approval!"})
    
    return render(request, "addbook.html")



def send_email(subject, recipient, plain_body, html_template, context):
    """
    Helper function to send emails with both plain text and HTML content.
    """
    html_content = render_to_string(html_template, context)
    email_message = EmailMultiAlternatives(
        subject=subject,
        body=plain_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    email_message.attach_alternative(html_content, "text/html")
    
    try:
        email_message.send(fail_silently=False)
    except Exception as e:
        
        print(f"Error sending email: {e}")
def approvebook(request, token):
    book = get_object_or_404(Book, approval_token=token)
    if not book.is_approved:
        book.is_approved = True
        book.earnings = 0 
        book.save()

        # Send approval email
        subject = "Your Book has been Approved!"
        plain_body = (
            f"Hi {book.submitted_by.username},\n"
            f"Congratulations! Your book '{book.title}' has been approved and is now live on our platform.\n"
            "Thank you for your valuable contribution to the E.Book Community!\n\n"
            "Best regards,\nThe E.Book Community Team"
        )
        send_email(
            subject=subject,
            recipient=book.submitted_by.email,
            plain_body=plain_body,
            html_template='emails/approval_notification.html',
            context={'book': book}
        )

        messages.success(request, "Book has been approved and is now available in the library.")
    else:
        messages.info(request, "Book is already approved.")

    return redirect('base:approval_status')  
 

def rejectbook(request, token):
    book = get_object_or_404(Book, approval_token=token)

    if book.is_approved:
        messages.warning(request, "Book is already approved and cannot be rejected.")
        return redirect('base:approval_status')  

    
    title = book.title
    submitted_by_email = book.submitted_by.email
    book.delete()

    # Send rejection email
    subject = "Your Book Submission has been Rejected"
    plain_body = f"Hi,\n\nUnfortunately, your book '{title}' has been rejected."
    send_email(
        subject=subject,
        recipient=submitted_by_email,
        plain_body=plain_body,
        html_template='emails/rejection_notification.html',
        context={'book_title': title}
    )

    messages.error(request, "Book submission has been rejected and removed.")
    return redirect('base:approval_status') 

def book_list(request):
    books = Book.objects.all()  # Fetch all book records from the database
    return render(request, 'index.html', {'books': books})


from django.shortcuts import render
from .models import Book, Note

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Book, Note
from decimal import Decimal

VIEWS_PER_RUPEE = 10  

from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from .models import Book, Note

# Define this constant in settings or views
VIEWS_PER_RUPEE = 10

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if not request.session.get(f'viewed_{book.id}', False):
        book.views += 1

        if book.is_approved:  
            book.earnings = Decimal(book.views // VIEWS_PER_RUPEE)

       
        book.save()

    
        request.session[f'viewed_{book.id}'] = True
    notes = Note.objects.filter(book=book)
    print(f"Earnings for book {book.title}: ₹{book.earnings}")
    return render(request, 'btech.html', {'book': book, 'notes': notes})






def Addbook(request):
    return render(request, "addbook.html")




"""


def book_detail(request, pk):
    # Get the book by its primary key (ID)
    book = get_object_or_404(Book, pk=pk)

    # Check if the user has viewed the book before in this session
    if not request.session.get(f'viewed_{book.id}', False):
        # If the user has not viewed the book, increment the view count
        book.views += 1
        book.save()
        # Mark the book as viewed in the session
        request.session[f'viewed_{book.id}'] = True

    # Fetch all notes associated with the book
    notes = Note.objects.filter(book=book)

    # Return the rendered template with the book details and its notes
    return render(request, 'btech.html', {'book': book, 'notes': notes})


"""


def save_note(request, book_id):
    try:
        data = json.loads(request.body)
        note_text = data.get('text', '').strip()

        if not note_text:
            return JsonResponse({'error': 'Note text cannot be empty.'}, status=400)

        book = get_object_or_404(Book, id=book_id, is_approved=True)

        # Get the existing note or create a new one
        note, _ = Note.objects.get_or_create(user=request.user, book=book)

        # Overwrite the note text with the new input
        note.text = note_text  
        note.save()

        return JsonResponse({
            'message': 'Note saved successfully.',
            'updated_at': note.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def update_note(request, book_id):
    try:
        data = json.loads(request.body)
        note_text = data.get('text', '').strip()

        if not note_text:
            return JsonResponse({'error': 'Note text cannot be empty.'}, status=400)

        book = get_object_or_404(Book, id=book_id, is_approved=True)

        # Get the note for the user and book
        note = get_object_or_404(Note, user=request.user, book=book)

        # Clean the input text
        note.text = note_text
        note.save()

        return JsonResponse({'message': 'Note updated successfully.', 'updated_at': note.updated_at.strftime('%Y-%m-%d %H:%M:%S')})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@require_POST
def delete_note(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id, is_approved=True)
        note = Note.objects.get(user=request.user, book=book)
        note.delete()
        return JsonResponse({'message': 'Note cleared successfully.'})
    except Note.DoesNotExist:
        return JsonResponse({'error': 'No existing note to delete.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from django.core.mail import EmailMessage



from django.core.mail import send_mail
from django.http import HttpResponse

def send_confirmation_email(request):
    try:
        send_mail(
            'Confirmation Email',
            'Thank you for registering!',
            'siddharthasiddhartha16@gmail.com',
            ['recipient_email@gmail.com'],
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")



#search
#from fuzzywuzzy import process



def searchbar(request):
    query = request.GET.get('search', '')
    results = []

    if query:
       
        results = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        ) | Book.objects.filter(
            description__icontains=query
        )  |Book.objects.filter(
            category__icontains=query
        )  |Book.objects.filter(
            selected_item__icontains=query
        )
        

    return render(request, 'searchbar.html', {'post': results})


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_items = sum(item.quantity for item in cart_items)  # Total quantity of all items
    cart_items_count = cart_items.count()  # Count of unique cart items
    return render(request, "cart.html", {
        "cart_items": cart_items, 
        "total_items": total_items,  # Total quantity of items
        "cart_items_count": cart_items_count  # Count of unique items in the cart
    })

from django.http import JsonResponse
from .models import CartItem, Book
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Use this only for testing; prefer CSRF protection in production.
def add_to_cart(request):
    if request.method == 'POST':
        try:
            book_id = request.POST.get('book_id')
            quantity = request.POST.get('quantity', 1)

            # Validate the input
            if not book_id:
                return JsonResponse({'error': 'Book ID is required'}, status=400)

            # Assuming you have a method to get the book
            book = Book.objects.get(id=book_id)
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                book=book,
                defaults={'quantity': quantity}
            )

            # Create or update the cart item
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                book=book,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += int(quantity)
                cart_item.save()

            return JsonResponse({'message': 'Item added to cart successfully'}, status=200)

        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


#remove cart view

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('base:cart')




#help page

def help(request):
    return render(request,"help.html")

def group(request):
    return render(request, "group.html")





def contact_view(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            complaint = form.cleaned_data['complaint']



    return render(request, 'contact.html', {'form': form, 'submitted': submitted})

import openai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import openai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatAPI(request):
    print(f"Received request method: {request.method}")  # Debugging log
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')

        # Ensure OpenAI API key is configured
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Use the key set in the .env file
        
        if not prompt:
            return JsonResponse({"error": "Prompt is required."}, status=400)

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=256,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )

            answer = response.choices[0].text.strip()
            return JsonResponse({"response": answer})

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"})

    return JsonResponse({"error": "Invalid request method. Please use POST."}, status=400)


@login_required  
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Create a Feedback instance but don't save it to the database yet
            feedback = form.save(commit=False)
            feedback.user = request.user  # Link feedback to the logged-in user
            feedback.save()  # Now save the feedback

            # Send confirmation email to the user
            send_mail(
                subject='Thank You for Your Feedback!',
                message = (
                    "Dear {},\n\n"
                    "We truly appreciate the time you took to provide us with your valuable feedback. "
                    "Your insights and suggestions help us grow and improve our services to better meet your needs.\n\n"
                    "If you have any further thoughts or concerns, please do not hesitate to reach out. "
                    "We are always here to assist you.\n\n"
                    "Thank you once again for being part of the E.Book Community. We look forward to continuing to serve you.\n\n"
                    "Best regards,\n"
                    "The E.Book Community Team"
                    ).format(request.user.username),

                from_email=settings.EMAIL_HOST_USER,  # Your email
                recipient_list=[request.user.email],  # Send to the user's email
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )

            return redirect('base:fsuccess')  # Redirect after successful submission
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})




def fsuccess(request):
    return render(request, 'fsuccess.html')






  # Use with caution, consider using CSRF token in production






#resukts



from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import User

def send_invitation(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        link = request.POST.get('link')

        try:
            # Get the user's email based on the provided username
            user = User.objects.get(username=username)
            recipient_email = user.email

            # Sender details (replace with actual sender name)
            sender_name = "JohnDoe"

            # Create a message with privacy and precautions
            subject = "Group Discussion Invitation"
            message = f"""
Hello {user.username},

You have been invited by {sender_name} to join a group discussion.

Join here: {link}

Please take note of the following precautions for a secure and smooth experience:

1. **Privacy**: Your personal information will remain confidential. Please do not share sensitive details during the session.
2. **Screen Sharing**: Ensure that no personal or confidential content is visible on your screen before you start sharing. It is advisable to use a clean workspace for better clarity and privacy.
3. **Conduct**: Respectful behavior is expected from all participants. Please avoid disruptive actions and be mindful of others.
4. **Technical Requirements**: Ensure that your device and internet connection are stable to avoid interruptions during the session. If you have any technical issues, contact support immediately.

We look forward to your participation and a fruitful discussion!

Best regards,  
{sender_name}
            """

            # Send the invitation email
            send_mail(subject, message, 'your-email@example.com', [recipient_email])

            return JsonResponse({'status': 'success'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'})
        except Exception as e:
            print("Error sending invitation:", e)  # Logging the exception
            return JsonResponse({'status': 'error', 'message': str(e)})






#lecture data 
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import LecturerApplicationForm
def lecturer_application(request):
    if request.method == 'POST':
        form = LecturerApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()

            # Send thank-you email
            subject = "Thank You for Applying to Work with E.Book Community"
            message = f"Dear {application.first_name},\n\nThank you for your interest in working with the E.Book Community team! We have received your application and will review your qualifications soon.\n\nBest regards,\nE.Book Community Team"
            recipient_list = [application.email]
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            except Exception as e:
                # Log the exception or print it for debugging
                print(f"Error sending email: {e}")

            return redirect('base:application_success')  # Redirect to a success page
        else:
            # Log form errors for debugging
            print(form.errors)
    else:
        form = LecturerApplicationForm()
    
    return render(request, 'lecturer_application.html', {'form': form})
  


def application_success(request):
    return render(request, 'application_success.html')





def meet(request):
    return render(request,"meet.html")




def request_class(request):
    if request.method == "POST":
        raw_time = request.POST.get("time")  # Format: YYYY-MM-DDTHH:MM
        topic = request.POST.get("topic")
        category = request.POST.get("category")

        # Handle time input
        if raw_time:
            try:
                preferred_time = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M")
            except ValueError:
                return HttpResponse("Invalid datetime format. Please try again.", status=400)
        else:
            # Default to the current time (immediate)
            preferred_time = now()

        # Save the class request
        class_request = ClassRequest(
            time=preferred_time,
            topic=topic,
            category=category,
            user=request.user  # Assuming the user is logged in
        )
        class_request.save()

        # Filter approved lecturers for the specific category
        lecturers = LecturerApplication.objects.filter(
            preferred_subjects__icontains=category,
            application_status='Approved'
        )

        if lecturers.exists():
            # Notify lecturers one by one until one accepts
            for lecturer in lecturers:
                subject = f"Class Request: {topic} in {category}"
                message = f"A user has requested a class on '{topic}' in the '{category}' category.\n"
                message += f"Preferred time: {preferred_time.strftime('%Y-%m-%d %H:%M')}.\n\n"
                message += "Please confirm by clicking one of the following links:\n"
                
                accept_url = request.build_absolute_uri(reverse('base:accept_class', args=[class_request.id]))
                reject_url = request.build_absolute_uri(reverse('base:reject_class', args=[class_request.id]))

                message += f"Accept: {accept_url}\nReject: {reject_url}\n"

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [lecturer.email],
                    fail_silently=False,
                )
                
                # Wait for lecturer response before notifying the next lecturer
                # Break the loop once a lecturer accepts
                break
        else:
            # No lecturers available for this category
            return HttpResponse("No approved lecturers available for this subject.", status=400)

        # Send confirmation email to the user
        confirmation_subject = "Class Request Received"
        confirmation_message = f"Dear {request.user.first_name},\n\n"
        confirmation_message += f"Thank you for requesting a class on '{topic}' in the '{category}' category.\n"
        confirmation_message += "We are working to assign a lecturer for your preferred time.\n\n"
        confirmation_message += "You will receive further updates shortly. Thank you for choosing us!"

        send_mail(
            confirmation_subject,
            confirmation_message,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )

        return HttpResponse("Class request submitted successfully. We are notifying approved lecturers.")
    return render(request, "request_class.html")




def accept_class(request, class_request_id):
    # Get the class request
    class_request = get_object_or_404(ClassRequest, id=class_request_id)

    # Check if the request has already been handled
    if class_request.responded:
        return HttpResponse("This request has already been responded to.", status=400)

    # Update the status to accepted
    class_request.status = 'accepted'
    class_request.responded = True  # Mark as handled
    class_request.save()

    # Send confirmation emails (as before)
    lecturer_confirmation_subject = f"Class Request Accepted: {class_request.topic}"
    lecturer_confirmation_message = f"Dear Lecturer,\n\n"
    lecturer_confirmation_message += f"Thank you for accepting the class request for '{class_request.topic}' in the '{class_request.category}' category.\n"
    lecturer_confirmation_message += f"The class is scheduled for: {class_request.time.strftime('%Y-%m-%d %H:%M')}.\n"
    lecturer_confirmation_message += "We look forward to your session!\n\n"
    send_mail(
        lecturer_confirmation_subject,
        lecturer_confirmation_message,
        settings.EMAIL_HOST_USER,
        [class_request.user.email],  # Notify the user
        fail_silently=False,
    )

    # Notify the user
    user_confirmation_subject = "Class Request Accepted"
    user_confirmation_message = f"Dear {class_request.user.first_name},\n\n"
    user_confirmation_message += f"Your class request for the topic '{class_request.topic}' has been accepted!\n"
    user_confirmation_message += f"The class is scheduled for {class_request.time.strftime('%Y-%m-%d %H:%M')}.\n"
    send_mail(
        user_confirmation_subject,
        user_confirmation_message,
        settings.EMAIL_HOST_USER,
        [class_request.user.email],  # Notify the user
        fail_silently=False,
    )

    return render(request, 'classaccept.html', {'class_request': class_request})

from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from base.models import ClassRequest, LecturerApplication
import random



def reject_class(request, class_request_id):
    class_request = get_object_or_404(ClassRequest, id=class_request_id)

    # Check if the request has already been handled
    if class_request.responded:
        return HttpResponse("This request has already been responded to.", status=400)

    if request.method == 'POST':
        # Update the class request as rejected
        class_request.status = 'rejected'
        class_request.responded = True
        class_request.save()

        # Attempt to reassign the class to another lecturer
        category = class_request.category
        lecturers = LecturerApplication.objects.filter(
            preferred_subjects__icontains=category,
            application_status='Approved'
        ).exclude(email=class_request.last_contacted_lecturer)

        if lecturers.exists():
            for lecturer in lecturers:
                subject = f"Class Request: {class_request.topic} in {category}"
                message = f"A user has requested a class on '{class_request.topic}' in the '{category}' category.\n"
                message += f"Preferred time: {class_request.time.strftime('%Y-%m-%d %H:%M')}.\n\n"
                message += "Please confirm by clicking one of the following links:\n"
                
                accept_url = request.build_absolute_uri(reverse('base:accept_class', args=[class_request.id]))
                reject_url = request.build_absolute_uri(reverse('base:reject_class', args=[class_request.id]))

                message += f"Accept: {accept_url}\nReject: {reject_url}\n"

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [lecturer.email],
                    fail_silently=False,
                )

                # Update the last contacted lecturer
                class_request.last_contacted_lecturer = lecturer.email
                class_request.save()
                break
        else:
            # Notify user about unavailability of lecturers
            user_subject = "Class Request Update"
            user_message = f"Dear {class_request.user.first_name},\n\n"
            user_message += f"We are sorry to inform you that all our lecturers are currently unavailable for your preferred time.\n"
            user_message += "Please reschedule your request at a later time.\n\nThank you for your understanding."

            send_mail(
                user_subject,
                user_message,
                settings.EMAIL_HOST_USER,
                [class_request.user.email],
                fail_silently=False,
            )

        return HttpResponse("Class reassigned or user notified about unavailability.")
    return render(request, 'class_rejection_reason.html', {'class_request': class_request})


def class_rejection_reason(request):
    return render(request,class_rejection_reason.html)


def send_class_request_email(class_request, lecturer):
    subject = f"Class Request: {class_request.topic}"
    message = f"""
    You have a class request:
    Topic: {class_request.topic}
    Time: {class_request.time}
    Category: {class_request.category}
    Please accept or reject this request.
    """
    email_from = 'your_email@example.com'
    recipient_list = [lecturer.email]
    send_mail(subject, message, email_from, recipient_list)








from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Book

@login_required
def profile(request):
    user = request.user
    books = Book.objects.filter(submitted_by=user)  # Fetch user's books
    total_earnings = sum(book.earnings for book in books)

    if request.method == 'POST':
        # Handle profile update
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username:
            user.username = username
        if email:
            user.email = email

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Avoid form resubmission on refresh

    # Render the profile page for GET requests
    return render(request, 'profile.html', {
        'user': user,
        'books': books,
        'total_earnings': total_earnings
    })



def setting_view(request):
    return render(request, 'setting.html')



def withdraw(request):
    return render(request, 'withdraw.html')

def about_us(request):
    return render(request, 'about_us.html')

#for displaying the element in the index page
"""
def display(request):
    add= display.objects.all()
    return render(request, 'index.html', {'add': add}) 
"""



#lecture dashboards for lectures views functiona

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

@login_required
def lecturer_dashboard(request):
    # Fetch only the class requests related to this lecturer
    lecturer = request.user
    class_requests = ClassRequest.objects.filter(
        category__icontains=lecturer.lecturerapplication.preferred_subjects,
        status='Pending'
    )
    return render(request, "lecturer_dashboard.html", {'class_requests': class_requests})

@login_required
def lecturer_accept_class(request, class_request_id):
    class_request = get_object_or_404(ClassRequest, id=class_request_id)
    class_request.status = 'Accepted'
    class_request.responded = True
    class_request.zoom_link = f"https://zoom.us/meeting/{class_request.id}"  # Example Zoom link
    class_request.save()

    # Notify the user
    subject = "Class Request Accepted"
    message = f"Dear {class_request.user.first_name},\n\nYour class request on '{class_request.topic}' in the '{class_request.category}' category has been accepted.\n"
    message += f"Zoom Link: {class_request.zoom_link}\n\nThank you!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [class_request.user.email], fail_silently=False)

    return redirect('base:lecturer_dashboard')

@login_required
def lecturer_reject_class(request, class_request_id):
    class_request = get_object_or_404(ClassRequest, id=class_request_id)
    class_request.status = 'Rejected'
    class_request.responded = True
    rejection_reason = request.POST.get('rejection_reason', 'No reason provided.')
    class_request.rejection_reason = rejection_reason
    class_request.save()

    # Notify the user
    subject = "Class Request Rejected"
    message = f"Dear {class_request.user.first_name},\n\nYour class request on '{class_request.topic}' in the '{class_request.category}' category has been rejected.\n"
    message += f"Reason: {rejection_reason}\n\nThank you!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [class_request.user.email], fail_silently=False)

    return redirect('base:lecturer_dashboard')

def lecture_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user has a linked LecturerApplication and if they are approved
            if hasattr(user, 'lecturerapplication') and user.lecturerapplication.is_lecturer:
                login(request, user)
                return redirect('base:lecturer_dashboard')  # Redirect to lecturer dashboard
            else:
                # User exists but is not an approved lecturer
                return render(request, "lecturer_login.html", {
                    "error": "You are not authorized to log in as a lecturer."
                })
        else:
            # Invalid username or password
            return render(request, "lecturer_login.html", {
                "error": "Invalid username or password."
            })
    return render(request, "lecturer_login.html")



from django.shortcuts import render
from .models import LecturerApplication

from django.contrib.auth.decorators import login_required

@login_required
def lec_profile(request):
    # Filter LecturerApplication records for the currently logged-in user
    data = LecturerApplication.objects.filter(user=request.user)
    context = {"data": data}
    return render(request, "lec_profile.html", context)


def edit_lecturer_profile(request,id):
    if request.method =="POST":
        email=  request.POST[email]
        phone= request.POST[phone]
        preferred_subjects= request.POST[preferred_subjects]
        preferred_time= request.POST[preferred_time]
        preferred_days= request.POST[preferred_days]
        languages= request.POST[languages]
        
        edit=LecturerApplication.objects.get(id=id)
        edit.email=email
        edit.phone=phone
        edit.preferred_subjects=preferred_subjects
        edit.preferred_time=preferred_time
        edit.preferred_days=preferred_days
        edit.languages=languages
        
        d=LecturerApplication.objects.get(id=id)
        context={"d": d}
        return render(request,lec_profile,context)
        
        
        
        
    
