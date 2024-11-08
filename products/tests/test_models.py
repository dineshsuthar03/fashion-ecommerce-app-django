import pytest
from django.contrib.auth.models import User
from products.models import Category, ColorVariant, SizeVariant, Product, ProductImage, Coupon, ProductReview, Wishlist
from django.db.utils import IntegrityError

# Fixtures
@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def category():
    return Category.objects.create(category_name="Electronics")

@pytest.fixture
def color_variant():
    return ColorVariant.objects.create(color_name="Red", price=20)

@pytest.fixture
def size_variant():
    return SizeVariant.objects.create(size_name="M", price=10)

@pytest.fixture
def product(category, color_variant, size_variant):
    product = Product.objects.create(
        product_name="Test Product",
        price=100,
        product_desription="This is a test product",
        category=category,
        newest_product=True
    )
    product.color_variant.add(color_variant)
    product.size_variant.add(size_variant)
    return product

@pytest.fixture
def product_image(product):
    return ProductImage.objects.create(product=product, image='test_image.jpg')

@pytest.fixture
def coupon():
    return Coupon.objects.create(coupon_code="DISCOUNT10", discount_amount=10, minimum_amount=500)

@pytest.fixture
def product_review(user, product):
    return ProductReview.objects.create(
        product=product,
        user=user,
        stars=5,
        content="Great product!"
    )

@pytest.fixture
def wishlist(user, product, size_variant):
    return Wishlist.objects.create(user=user, product=product, size_variant=size_variant)

# Test Cases

# 1. Test Category Model
@pytest.mark.django_db
def test_category_model(category):
    assert category.category_name == "Electronics"
    assert category.slug == "electronics"

# 2. Test ColorVariant Model
@pytest.mark.django_db
def test_color_variant_model(color_variant):
    assert color_variant.color_name == "Red"
    assert color_variant.price == 20

# 3. Test SizeVariant Model
@pytest.mark.django_db
def test_size_variant_model(size_variant):
    assert size_variant.size_name == "M"
    assert size_variant.price == 10

# 4. Test Product Model
@pytest.mark.django_db
def test_product_model(product, category, color_variant, size_variant):
    assert product.product_name == "Test Product"
    assert product.price == 100
    assert product.category == category
    assert color_variant in product.color_variant.all()
    assert size_variant in product.size_variant.all()

# 5. Test Product Model - get_product_price_by_size
@pytest.mark.django_db
def test_get_product_price_by_size(product, size_variant):
    price = product.get_product_price_by_size("M")
    assert price == product.price + size_variant.price

# 6. Test Product Model - get_rating
@pytest.mark.django_db
def test_get_product_rating(product, product_review):
    assert product.get_rating() == 5  # Since the review has a 5-star rating

# 7. Test ProductImage Model
@pytest.mark.django_db
def test_product_image_model(product_image):
    assert product_image.product.product_name == "Test Product"
    assert product_image.image == 'test_image.jpg'

# 8. Test Coupon Model
@pytest.mark.django_db
def test_coupon_model(coupon):
    assert coupon.coupon_code == "DISCOUNT10"
    assert coupon.discount_amount == 10
    assert coupon.minimum_amount == 500

# 9. Test ProductReview Model
@pytest.mark.django_db
def test_product_review_model(product_review, product, user):
    assert product_review.product == product
    assert product_review.user == user
    assert product_review.stars == 5
    assert product_review.content == "Great product!"
    assert product_review.date_added is not None

# 10. Test Wishlist Model
@pytest.mark.django_db
def test_wishlist_model(wishlist, user, product, size_variant):
    assert wishlist.user == user
    assert wishlist.product == product
    assert wishlist.size_variant == size_variant
    assert str(wishlist) == f'{user.username} - {product.product_name} - {size_variant.size_name}'

# 11. Test Wishlist Model - Unique Constraint
@pytest.mark.django_db
def test_wishlist_unique_constraint(user, product, size_variant):
    # Trying to create two wishlist entries with the same product and size_variant should raise an IntegrityError
    Wishlist.objects.create(user=user, product=product, size_variant=size_variant)
    with pytest.raises(IntegrityError):
        Wishlist.objects.create(user=user, product=product, size_variant=size_variant)
