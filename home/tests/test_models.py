from django.test import TestCase
from django.contrib.auth.models import User
from home.models import ShippingAddress, ShippingAddressForm
from django.urls import reverse

# Test case for the ShippingAddress model
class ShippingAddressModelTest(TestCase):
    def setUp(self):
        # Create a user for the address
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_shipping_address_creation(self):
        # Create a shipping address
        address = ShippingAddress.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            street='123 Main St',
            street_number='Apt 4B',
            zip_code='12345',
            city='Sample City',
            country='US',
            phone='123-456-7890',
            current_address=True
        )

        # Check if the address is created correctly
        self.assertEqual(address.first_name, 'John')
        self.assertEqual(address.last_name, 'Doe')
        self.assertEqual(address.street, '123 Main St')
        self.assertEqual(address.zip_code, '12345')

    def test_string_representation(self):
        address = ShippingAddress.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            street='123 Main St',
            street_number='Apt 4B',
            zip_code='12345',
            city='Sample City',
            country='US',
            phone='123-456-7890',
            current_address=True
        )
        self.assertEqual(str(address), 'Shipping address for testuser: 123 Main St Apt 4B, Sample City')

    def test_current_address_logic(self):
        # Create two addresses for the same user
        address1 = ShippingAddress.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            street='123 Main St',
            street_number='Apt 4B',
            zip_code='12345',
            city='Sample City',
            country='US',
            phone='123-456-7890',
            current_address=True
        )

        address2 = ShippingAddress.objects.create(
            user=self.user,
            first_name='Jane',
            last_name='Doe',
            street='456 Other St',
            street_number='Apt 1A',
            zip_code='54321',
            city='Another City',
            country='US',
            phone='987-654-3210',
            current_address=False
        )

        # Only the first address should be marked as current
        self.assertTrue(address1.current_address)
        self.assertFalse(address2.current_address)

        # Now, mark address2 as current and address1 as not current
        address2.current_address = True
        address2.save()

        address1.refresh_from_db()

        self.assertFalse(address1.current_address)
        self.assertTrue(address2.current_address)

    def test_get_absolute_url(self):
        # Create a shipping address
        address = ShippingAddress.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            street='123 Main St',
            street_number='Apt 4B',
            zip_code='12345',
            city='Sample City',
            country='US',
            phone='123-456-7890',
            current_address=True
        )

        # Check if the absolute URL is correct
        self.assertEqual(address.get_absolute_url(), reverse('shipping-address'))

# Test case for ShippingAddressForm
class ShippingAddressFormTest(TestCase):
    def setUp(self):
        # Create a user for the address form
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_valid_form(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'street': '123 Main St',
            'street_number': 'Apt 4B',
            'zip_code': '12345',
            'city': 'Sample City',
            'country': 'US',
            'phone': '123-456-7890'
        }

        form = ShippingAddressForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_field(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'street': '123 Main St',
            'zip_code': '12345',
            'city': 'Sample City',
            'country': 'US',
            'phone': '123-456-7890'
        }
        form = ShippingAddressForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('street_number', form.errors)

    def test_save_address_logic(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'street': '123 Main St',
            'street_number': 'Apt 4B',
            'zip_code': '12345',
            'city': 'Sample City',
            'country': 'US',
            'phone': '123-456-7890',
            'save_address': True
        }

        form = ShippingAddressForm(data=form_data)
        form.instance.user = self.user

        # Save the form and check if the current_address is set to True
        shipping_address = form.save()

        self.assertTrue(shipping_address.current_address)

    def test_save_address_not_checked(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'street': '123 Main St',
            'street_number': 'Apt 4B',
            'zip_code': '12345',
            'city': 'Sample City',
            'country': 'US',
            'phone': '123-456-7890',
            'save_address': False
        }

        form = ShippingAddressForm(data=form_data)
        form.instance.user = self.user

        # Save the form and check if the current_address is False
        shipping_address = form.save()

        self.assertFalse(shipping_address.current_address)

    def test_current_address_validation(self):
        # Create a shipping address and mark it as current
        ShippingAddress.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            street='123 Main St',
            street_number='Apt 4B',
            zip_code='12345',
            city='Sample City',
            country='US',
            phone='123-456-7890',
            current_address=True
        )

        # Try to create another address with the same user and mark it as current
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'street': '456 Other St',
            'street_number': 'Apt 1A',
            'zip_code': '54321',
            'city': 'Another City',
            'country': 'US',
            'phone': '987-654-3210',
            'save_address': True
        }

        form = ShippingAddressForm(data=form_data)
        form.instance.user = self.user

        self.assertFalse(form.is_valid())
        self.assertIn('save_address', form.errors)
