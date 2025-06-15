from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Create your models here.

ghana_card_validator = RegexValidator(
    regex=r'^GHA-\d{9}-\d$',
    message='Ghana Card must follow the format: GHA-123456789-1'
)


class CustomUserManager(BaseUserManager):
    """Manager for CustomUser"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a 'CustomUser' with an email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Use the built-in method to hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a 'CustomUser' with superuser permissions."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User Model"""
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(null=True, default="avatar.png")
    contact = models.CharField(max_length=10, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use email as the username
    REQUIRED_FIELDS = []  # Fields required when creating a user via the createsuperuser command

    def __str__(self):
        return self.email

class Bank(models.Model):
    bank_name = models.CharField(max_length=254, unique=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bank_name

class Program(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Survey(models.Model):
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description}"

class SurveyResponse(models.Model):
    TITLE_CHOICES = [('Mr.', 'Mr.'), ('Miss.', 'Miss.'), ('Mrs.', 'Mrs.')]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    STATUS_CHOICES = [('Active', 'Active'), ('Deffered', 'Deffered'), ('Dismissed', 'Dismissed')]
    ACCOUNT_TYPE_CHOICES = [('Savings Account', 'Savings Account'), ('Current Account', 'Current Account')]
    NATIONALITY_CHOICES = [('GHANAIAN', 'GHANAIAN'), ('OTHER', 'OTHER')]
    LEVEL_CHOICES = [(100, 'Level 100'), (200, 'Level 200'), (300, 'Level 300'), (400, 'Level 400')]
    ADMISSION_YEAR_CHOICES = [(str(y), str(y)) for y in range(2020, 2025)] + [('Other', 'Other')]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    index_number = models.CharField(max_length=20, unique=True, verbose_name="Index Number")
    title = models.CharField(max_length=5, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    middle_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Middle Name(s)")
    surname = models.CharField(max_length=100)  
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    ghana_card = models.CharField(max_length=25, verbose_name="Ghana Card Number", help_text="e.g. GHA-12345789-1", validators=[ghana_card_validator])
    ssnit_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="SSNIT Number")
    nationality = models.CharField(max_length=20, choices=NATIONALITY_CHOICES)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, verbose_name="Program of Study")
    level = models.IntegerField(choices=LEVEL_CHOICES)
    year_admitted = models.CharField(max_length=10, choices=ADMISSION_YEAR_CHOICES, verbose_name="Year Admitted")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Student Status")
    email = models.EmailField()
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, verbose_name="Bank Name")
    bank_branch = models.CharField(max_length=100, verbose_name="Bank Branch", help_text="Where the account was created")
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, verbose_name="Account Type")
    account_number = models.CharField(max_length=20, verbose_name="Bank Account Number")
    full_name = models.CharField(max_length=200, verbose_name="Full Name", help_text="Full name as it appears on your bank account")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.index_number} - {self.full_name}"
    
