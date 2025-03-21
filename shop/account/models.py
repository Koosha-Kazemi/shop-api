from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from phonenumber_field.modelfields import PhoneNumberField


class Customer(AbstractUser):
    """
    A custom user model representing a customer in the system.
    This model extends Django's built-in AbstractUser to add additional fields.
    """

    GENDERS = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    first_name = models.CharField(
        max_length=30,
        verbose_name='First Name',
        help_text='Enter the customer\'s first name.'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Last Name',
        help_text='Enter the customer\'s last name.'
    )
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name='Phone Number',
        help_text='Enter the customer\'s phone number (must start with 09).'
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDERS,
        blank=True,
        null=True,
        verbose_name='Gender',
        help_text='Select the customer\'s gender.'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Is Verified',
        help_text='Indicates whether the customer is verified.'
    )
    profile_image = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        verbose_name='Profile Image',
        help_text='Upload the customer\'s profile image.'
    )
    birth_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Birth Date',
        help_text='Enter the customer\'s birth date.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated',
        help_text='The date and time when the customer\'s profile was last updated.'
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'