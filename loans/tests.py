from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import CommentForm
from loans.models import *
from loans.views import *
from django.urls import reverse, resolve

class TestCommentForm(TestCase):
    """Test field of CommentForm"""

    def test_check_commentform_no_data(self):
        """Test Commentform as empty"""
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors.keys())
        self.assertEquals(len(form.errors), 1)

    def test_check_comment_form_is_required(self):
        """Test Commentform as required"""
        form = CommentForm(data={'comment': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors.keys())
        self.assertEquals(form.errors['comment'][0], 'This field is required.')

    def test_check_comment_form_is_not_required(self):
        """Test Commentform with value"""
        form = CommentForm(data={'comment': 'Test Commented'})
        self.assertTrue(form.is_valid())

    def test_fields_are_explicit_in_commentform_meta(self):
        """Test Commentform parameters are not changed"""
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ('comment',))

class TestViews(TestCase):
    """Test of behavior of views without login"""

    def test_get_book_list(self):
        """ Test access to home page with list of books not login"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_search(self):
        """ Test navbar search not login"""
        response = self.client.post("/", {"search": "Asimov"})
        self.assertEqual(response.status_code, 200)

    def test_loan_redirect_non_login(self):
        """ Test redirect on loans without login"""
        response = self.client.get('/loans')
        self.assertEqual(response.status_code, 301)

    def test_loan_redirect_from_bookdetail_add_reserved(self):
        """ Test redirect on loans with action params (not login)"""
        response = self.client.post("/loans", {"action": "add_reserved"})
        self.assertEqual(response.status_code, 301)

class TestViewsLogged(TestCase):
    """Test views behavior with login"""

    def setUp(self):
        """ Setup test """
        username = "demouser"
        password = "£Roy234"
        user_model = get_user_model()
        # Create user
        self.user = user_model.objects.create_user(
            username=username,
            password=password,
            is_superuser=True
        )
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_get_book_list(self):
        """ Test access to home page with list of books with login"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_search(self):
        """ Test navbar search with login"""
        response = self.client.post("/", {"search": "Asimov"})
        self.assertEqual(response.status_code, 200)

    def test_loan_redirect_non_login(self):
        """ Test redirect on loans with login"""
        response = self.client.get('/loans')
        self.assertEqual(response.status_code, 301)

    def test_loan_redirect_from_bookdetail_add_reserved(self):
        """ Test redirect on loans with action params (with login)"""
        response = self.client.post("/loans", {"action": "add_reserved"})
        self.assertEqual(response.status_code, 301)


class TestUrls(TestCase):
    """
    Class to test the urls
    """

    def setUp(self):
        """Login"""
        self.user = get_user_model().objects.create_user(
            username="demouser", password="£Roy234"
        )
        self.client = Client()

    def test_home_page_url(self):
        """Test the reverse of home"""
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, BookList)

    def test_book_page_url(self):
        """Test the reverse of book_detail"""
        url = reverse('book_detail', args=['some-slug'])
        self.assertEqual(resolve(url).func.view_class, BookDetail)

    def test_loan_page_url(self):
        """Test the reverse of loan_detail"""
        url = reverse('loan_detail')
        self.assertEqual(resolve(url).func.view_class, LoanDetail)

class TestModels(TestCase):
    """
    Class to test models
    """

    def setUp(self):
        """Login"""
        self.user = get_user_model().objects.create_user(
            username="demouser", password="£Roy234"
        )
        self.client = Client()

    def test_book_model_str(self):
        """Test Model of book and __str__ result"""
        book = Book(title='My Title', author="My Author")
        self.assertEqual(str(book), f"{book.author} - {book.title} ({book.number_of_items} books, {book.items_to_loan} to loans)")
        



