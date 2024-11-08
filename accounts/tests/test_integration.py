import json
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase, Client
from accounts.models import Profile, Cart, CartItem
from products.models import Product, SizeVariant
from django.contrib.messages import get_messages


class AccountsIntegrationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass", email="test@example.com")
        self.profile = Profile.objects.create(user=self.user, is_email_verified=True)
        self.product = Product.objects.create(name="Test Product", price=100)
        self.size_variant = SizeVariant.objects.create(size_name="M", product=self.product)
        self.cart = Cart.objects.create(user=self.user, is_paid=False)

    def test_register_page_success(self):
        response = self.client.post(reverse('register_page'), {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'new@example.com',
            'password': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page_success(self):
        response = self.client.post(reverse('login_page'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertIn('_auth_user_id', self.client.session)  # Check if user is authenticated

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('add_to_cart', args=[self.product.uid]), {
            'size': 'M'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to cart page after adding
        cart_item = CartItem.objects.filter(cart=self.cart, product=self.product, size_variant=self.size_variant)
        self.assertTrue(cart_item.exists())  # Check if item is added to the cart

    def test_apply_coupon_to_cart(self):
        self.client.login(username='testuser', password='testpass')
        self.cart.is_paid = False
        self.cart.save()
        response = self.client.post(reverse('cart'), {
            'coupon': 'TESTCOUPON'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)  # Redirect after applying coupon
        self.assertIn("Invalid coupon code.", str(messages[0]))  # Check feedback message

    def test_order_history_access(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/order_history.html')

    def test_profile_view_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('profile_view', args=['testuser']), {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedFirst')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_delete_account(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)  # Redirect after account deletion
        self.assertFalse(User.objects.filter(username='testuser').exists())  # User should be deleted
