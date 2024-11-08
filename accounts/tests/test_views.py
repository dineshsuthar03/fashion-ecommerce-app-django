from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile, Cart, CartItem, Order
from products.models import Product, SizeVariant
from home.models import ShippingAddress
from unittest.mock import patch

class AccountsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = Profile.objects.create(user=self.user, is_email_verified=True)
        self.product = Product.objects.create(name="Test Product", price=100.00)
        self.size_variant = SizeVariant.objects.create(size_name="M", product=self.product)

    def test_login_page_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_page_view_post_successful(self):
        self.user.profile.is_email_verified = True
        self.user.profile.save()
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(self.client.session['_auth_user_id'])

    def test_register_page_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_page_view_post(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_logout_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user_logout'))
        self.assertRedirects(response, reverse('index'))

    def test_add_to_cart_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('add_to_cart', args=[self.product.uid]), {'size': 'M'})
        self.assertRedirects(response, reverse('cart'))
        self.assertTrue(CartItem.objects.filter(cart__user=self.user, product=self.product).exists())

    def test_update_cart_item_view(self):
        self.client.login(username='testuser', password='password123')
        cart = Cart.objects.create(user=self.user, is_paid=False)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, size_variant=self.size_variant, quantity=1)
        response = self.client.post(reverse('update_cart_item'), json.dumps({
            'cart_item_id': cart_item.uid,
            'quantity': 2
        }), content_type="application/json")
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(response.json(), {"success": True})

    def test_remove_cart_view(self):
        self.client.login(username='testuser', password='password123')
        cart = Cart.objects.create(user=self.user, is_paid=False)
        cart_item = CartItem.objects.create(cart=cart, product=self.product, size_variant=self.size_variant)
        response = self.client.get(reverse('remove_cart', args=[cart_item.uid]))
        self.assertRedirects(response, reverse('cart'))
        self.assertFalse(CartItem.objects.filter(uid=cart_item.uid).exists())

    @patch('accounts.views.send_account_activation_email')
    def test_activate_email_account_view(self, mock_send_email):
        self.user.profile.email_token = 'sample-token'
        self.user.profile.save()
        response = self.client.get(reverse('activate_email_account', args=['sample-token']))
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.is_email_verified)
        self.assertRedirects(response, reverse('login'))

    def test_profile_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile_view', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_change_password_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('change_password'), {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        self.assertRedirects(response, reverse('profile_view', args=['testuser']))

    def test_order_history_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/order_history.html')

    def test_delete_account_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('delete_account'))
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

