import pytest
from django.contrib.auth.models import User
from products.models import Product, ColorVariant, SizeVariant, Coupon
from accounts.models import Profile, Cart, CartItem, Order, OrderItem

@pytest.mark.django_db
def test_profile_get_cart_count():
    user = User.objects.create(username="testuser")
    profile = Profile.objects.create(user=user)
    assert profile.get_cart_count() == 0

@pytest.mark.django_db
def test_profile_save():
    user = User.objects.create(username="testuser")
    profile = Profile.objects.create(user=user, profile_image="old_image.jpg")
    profile.profile_image = "new_image.jpg"
    profile.save()
    # You can add additional checks here if required.

@pytest.mark.django_db
def test_cart_get_cart_total():
    user = User.objects.create(username="testuser")
    cart = Cart.objects.create(user=user)
    product = Product.objects.create(name="Test Product", price=100)
    CartItem.objects.create(cart=cart, product=product, quantity=2)
    assert cart.get_cart_total() == 200  # 100 * 2

@pytest.mark.django_db
def test_cart_get_cart_total_price_after_coupon():
    user = User.objects.create(username="testuser")
    cart = Cart.objects.create(user=user)
    product = Product.objects.create(name="Test Product", price=100)
    coupon = Coupon.objects.create(discount_amount=50, minimum_amount=100)
    CartItem.objects.create(cart=cart, product=product, quantity=1)
    cart.coupon = coupon
    assert cart.get_cart_total_price_after_coupon() == 50

@pytest.mark.django_db
def test_cart_item_get_product_price():
    product = Product.objects.create(name="Test Product", price=100)
    color_variant = ColorVariant.objects.create(price=10)
    size_variant = SizeVariant.objects.create(price=20)
    cart_item = CartItem.objects.create(product=product, color_variant=color_variant, size_variant=size_variant, quantity=2)
    assert cart_item.get_product_price() == 260  # 100*2 + 10 + 20*2

@pytest.mark.django_db
def test_order_get_order_total_price():
    user = User.objects.create(username="testuser")
    order = Order.objects.create(user=user, order_total_price=300)
    assert order.get_order_total_price() == 300

@pytest.mark.django_db
def test_order_item_get_total_price():
    product = Product.objects.create(name="Test Product", price=100)
    size_variant = SizeVariant.objects.create(price=20)
    color_variant = ColorVariant.objects.create(price=10)
    order_item = OrderItem.objects.create(product=product, size_variant=size_variant, color_variant=color_variant, quantity=2)
    assert order_item.get_total_price() == 260  # 100*2 + 10 + 20*2
