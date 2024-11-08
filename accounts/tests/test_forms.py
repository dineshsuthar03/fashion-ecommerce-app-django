# accounts/tests/test_forms.py
import pytest
from django.contrib.auth.models import User
from accounts.models import Profile
from home.models import ShippingAddress
from accounts.forms import (
    UserProfileForm,
    UserUpdateForm,
    ShippingAddressForm,
    CustomPasswordChangeForm
)


@pytest.mark.django_db
def test_user_profile_form_valid_data():
    form = UserProfileForm(data={
        'bio': 'This is a test bio',
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_user_profile_form_empty_data():
    form = UserProfileForm(data={})
    assert form.is_valid()  # Because `bio` is optional
    assert form.cleaned_data.get('bio') is None


@pytest.mark.django_db
def test_user_update_form_valid_data():
    user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
    form = UserUpdateForm(data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    })
    assert form.is_valid()
    assert form.cleaned_data['first_name'] == 'John'
    assert form.cleaned_data['email'] == 'john.doe@example.com'


@pytest.mark.django_db
def test_user_update_form_invalid_data():
    form = UserUpdateForm(data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'invalid-email'
    })
    assert not form.is_valid()
    assert 'email' in form.errors


@pytest.mark.django_db
def test_shipping_address_form_valid_data():
    user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
    form = ShippingAddressForm(data={
        'address_line_1': '123 Main St',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'Test Country',
        'zip_code': '12345'
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_shipping_address_form_exclude_user():
    form = ShippingAddressForm()
    excluded_fields = form.Meta.exclude
    assert 'user' in excluded_fields


@pytest.mark.django_db
def test_custom_password_change_form():
    user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
    form = CustomPasswordChangeForm(user=user)
    assert form.fields['old_password'].widget.attrs['class'] == 'form-control'
    assert form.fields['new_password1'].widget.attrs['class'] == 'form-control'
    assert form.fields['new_password2'].widget.attrs['class'] == 'form-control'
    assert form.fields['old_password'].label == 'Current password'
    assert form.fields['new_password1'].label == 'New password'
    assert form.fields['new_password2'].label == 'New password confirmation'
