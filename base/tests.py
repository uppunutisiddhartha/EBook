from django.test import TestCase, Client
from .models import Book, Note
import json
from django.urls import reverse
from django.contrib.auth.models import User




from django.test import TestCase
from django.contrib.auth.models import User
from .models import Student

class StudentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Student.objects.create(user=user, firstname='Test', lastname='User', mail='test@example.com')

    def test_student_creation(self):
        student = Student.objects.get(user__username='testuser')
        self.assertEqual(student.firstname, 'Test')
        self.assertEqual(student.lastname, 'User')
        self.assertEqual(student.mail, 'test@example.com')


class SaveNoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            author='Author Name',
            description='A test book.',
            category='library',
            selected_item='history'
        )
        self.save_note_url = reverse('save-note', args=[self.book.id])

    def test_save_note_authenticated_user_creates_note(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            self.save_note_url,
            data=json.dumps({'text': 'This is a test note.'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.first()
        self.assertEqual(note.text, 'This is a test note.')
        self.assertEqual(note.user, self.user)
        self.assertEqual(note.book, self.book)

    def test_save_note_authenticated_user_updates_note(self):
        Note.objects.create(user=self.user, book=self.book, text='Initial note.')
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            self.save_note_url,
            data=json.dumps({'text': 'Updated note.'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.first()
        self.assertEqual(note.text, 'Updated note.')

    def test_save_note_unauthenticated_user(self):
        response = self.client.post(
            self.save_note_url,
            data=json.dumps({'text': 'This should not be saved.'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertEqual(Note.objects.count(), 0)

    def test_save_note_empty_text(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(
            self.save_note_url,
            data=json.dumps({'text': ''}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(Note.objects.count(), 0)