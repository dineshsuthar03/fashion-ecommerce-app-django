import pytest
from django.contrib.auth.models import User
from products.models import Product, ProductReview
from products.forms import ReviewForm

# Fixtures
@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def product():
    return Product.objects.create(
        product_name="Test Product",
        price=100,
        product_desription="This is a test product",
        newest_product=True
    )

# Test Case

# 1. Test ReviewForm - Create new review
@pytest.mark.django_db
def test_review_form_create(user, product):
    form_data = {
        'stars': 4,
        'content': 'Great product!'
    }
    form = ReviewForm(data=form_data)
    assert form.is_valid()  # Check if form is valid

    # Save the form and check if a ProductReview is created
    review = form.save(commit=False)
    review.product = product
    review.user = user
    review.save()

    # Verify the review was created successfully
    assert ProductReview.objects.count() == 1
    review = ProductReview.objects.first()
    assert review.stars == 4
    assert review.content == 'Great product!'
    assert review.product == product
    assert review.user == user

# 2. Test ReviewForm - Update existing review
@pytest.mark.django_db
def test_review_form_update(user, product):
    # Create an initial review
    review = ProductReview.objects.create(
        product=product,
        user=user,
        stars=3,
        content="Okay product."
    )

    # Update the review
    form_data = {
        'stars': 5,
        'content': 'Excellent product!'
    }
    form = ReviewForm(data=form_data, instance=review)
    assert form.is_valid()  # Check if form is valid

    # Save the form and verify the review is updated
    updated_review = form.save()
    assert updated_review.stars == 5
    assert updated_review.content == 'Excellent product!'
    assert updated_review.product == product
    assert updated_review.user == user

# 3. Test ReviewForm - Invalid form data (missing required fields)
@pytest.mark.django_db
def test_review_form_invalid(user, product):
    form_data = {
        'stars': 5,
        'content': ''  # Content is empty, should be invalid
    }
    form = ReviewForm(data=form_data)
    assert not form.is_valid()  # Check if form is invalid
    assert 'content' in form.errors  # Check if there's a validation error for 'content'
