import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, SizeVariant, Wishlist, ProductReview
from accounts.models import Cart, CartItem
from django.contrib.messages import get_messages
from django.test import Client

# Fixtures
@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def product():
    return Product.objects.create(name="Test Product", price=100, uid="12345", slug="test-product")

@pytest.fixture
def size_variant():
    return SizeVariant.objects.create(size_name="M", price=10)

@pytest.fixture
def wishlist(user, product, size_variant):
    return Wishlist.objects.create(user=user, product=product, size_variant=size_variant)

# Test Cases

# 1. Test `get_product` View
@pytest.mark.django_db
def test_get_product_view(user, product, size_variant):
    client = Client()
    client.login(username='testuser', password='password')
    
    # Creating a review for the product
    ProductReview.objects.create(product=product, user=user, review="Great product!", rating=5)
    
    url = reverse('get_product', kwargs={'slug': product.slug})
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'product' in response.context
    assert response.context['product'] == product
    assert response.context['rating_percentage'] == 100  # since it's a 5-star review
    assert 'review_form' in response.context
    assert 'related_products' in response.context

# 2. Test Adding to Wishlist
@pytest.mark.django_db
def test_add_to_wishlist(user, product, size_variant):
    client = Client()
    client.login(username='testuser', password='password')

    url = reverse('add_to_wishlist', kwargs={'uid': product.uid}) + f'?size={size_variant.size_name}'
    response = client.get(url)

    assert response.status_code == 302  # redirects to wishlist
    assert Wishlist.objects.filter(user=user, product=product, size_variant=size_variant).exists()

    # Check for success message in the response
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Product added to Wishlist!" in messages

# 3. Test Removing from Wishlist
@pytest.mark.django_db
def test_remove_from_wishlist(user, wishlist):
    client = Client()
    client.login(username='testuser', password='password')

    url = reverse('remove_from_wishlist', kwargs={'uid': wishlist.product.uid}) + f'?size={wishlist.size_variant.size_name}'
    response = client.get(url)

    assert response.status_code == 302  # redirects to wishlist
    assert not Wishlist.objects.filter(user=user, product=wishlist.product).exists()

    # Check for success message in the response
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Product removed from wishlist!" in messages

# 4. Test Wishlist View
@pytest.mark.django_db
def test_wishlist_view(user, wishlist):
    client = Client()
    client.login(username='testuser', password='password')

    url = reverse('wishlist')
    response = client.get(url)

    assert response.status_code == 200
    assert 'wishlist_items' in response.context
    assert wishlist in response.context['wishlist_items']

# 5. Test Moving to Cart
@pytest.mark.django_db
def test_move_to_cart(user, wishlist, size_variant):
    client = Client()
    client.login(username='testuser', password='password')

    # Adding product to cart
    url = reverse('move_to_cart', kwargs={'uid': wishlist.product.uid})
    response = client.get(url)

    # Check if the product was moved to the cart
    cart_item = CartItem.objects.filter(cart__user=user, product=wishlist.product).first()

    assert response.status_code == 302  # redirects to cart
    assert cart_item is not None
    assert cart_item.quantity == 1  # since it's the first time adding the product to cart

    # Check for success message
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert "Product moved to cart successfully!" in messages
