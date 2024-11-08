import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from home.models import ShippingAddress
from django.test import Client
from products.models import Product, Category
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from unittest.mock import patch


# Fixtures
@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def shipping_address_data():
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'street': '123 Main St',
        'street_number': 'A1',
        'zip_code': '12345',
        'city': 'Sample City',
        'country': 'US',
        'phone': '555-555-5555',
        'save_address': True,
    }


@pytest.fixture
def products():
    category = Category.objects.create(category_name="Electronics")
    product1 = Product.objects.create(product_name="Product 1", price=100.00, category=category)
    product2 = Product.objects.create(product_name="Product 2", price=200.00, category=category)
    return [product1, product2]


@pytest.fixture
def product_search_data():
    return {'q': 'Product 1'}


# Test Case 1: Test Index View - Product Filtering and Pagination
@pytest.mark.django_db
def test_index_view(user, products):
    client = Client()
    
    # Test default index view
    url = reverse('home:index')  # Use the actual URL name for the view
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == 2  # Two products created in the fixture
    
    # Test filtering by category
    url = reverse('home:index') + "?category=Electronics"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == 2
    
    # Test sorting by price (ascending)
    url = reverse('home:index') + "?sort=priceAsc"
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['selected_sort'] == 'priceAsc'
    
    # Test pagination (Assuming 1 product per page)
    url = reverse('home:index') + "?page=1"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == 2


# Test Case 2: Test Product Search View
@pytest.mark.django_db
def test_product_search_view(user, product_search_data, products):
    client = Client()

    # Test valid search query
    url = reverse('home:product_search') + f"?q={product_search_data['q']}"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == 1  # Only "Product 1" should match the query
    
    # Test invalid search query (No results)
    url = reverse('home:product_search') + "?q=NonexistentProduct"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == 0  # No products should match the query


# Test Case 3: Test Contact View - Valid Email
@pytest.mark.django_db
@patch('django.core.mail.send_mail')  # Mock send_mail to avoid sending emails during tests
def test_contact_view_valid_email(user, product_search_data):
    client = Client()

    # Test sending a message with valid email
    contact_data = {
        'message-name': 'John',
        'message-lname': 'Doe',
        'message-email': 'john.doe@example.com',
        'message': 'This is a test message.',
    }
    
    url = reverse('home:contact')
    response = client.post(url, contact_data)

    # Check if the email is sent
    send_mail.assert_called_once()

    # Check if success message is shown
    assert response.status_code == 302  # Should redirect after form submission
    assert "Thank you for your message" in response.cookies


# Test Case 4: Test Contact View - Invalid Email
@pytest.mark.django_db
def test_contact_view_invalid_email(user, product_search_data):
    client = Client()

    # Test sending a message with invalid email
    contact_data = {
        'message-name': 'John',
        'message-lname': 'Doe',
        'message-email': 'invalid-email',
        'message': 'This is a test message.',
    }
    
    url = reverse('home:contact')
    response = client.post(url, contact_data)

    # Check if error message is shown
    assert response.status_code == 302  # Should redirect after form submission
    assert "Invalid Email Address!" in response.cookies


# Test Case 5: Test Unauthorized Access to Shipping Address View
@pytest.mark.django_db
def test_shipping_address_view_unauthorized():
    # Create an unauthenticated client
    client = Client()
    
    url = reverse('shipping-address')
    
    # Try to access the shipping address view without logging in
    response = client.get(url)
    
    # Verify the response is a redirect to login page
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/?next=')
