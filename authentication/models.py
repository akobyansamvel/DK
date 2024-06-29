from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import CustomUserManager  # Import the CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = [
        ("Мужской", "Мужской"),
        ("Женский", "Женский"),
    ]
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    email = models.EmailField(verbose_name='Адрес эл. почты', max_length=255, unique=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=15, unique=True)
    sex = models.CharField(verbose_name="Пол", choices=SEX_CHOICES, max_length=7)
    
    is_active = models.BooleanField(verbose_name='Активирован', default=False)
    is_staff = models.BooleanField(verbose_name='Модерация', default=False)
    is_superuser = models.BooleanField(verbose_name='Администратор', default=False)
    can_help = models.BooleanField(verbose_name='Волонтер', default=False)
    need_help = models.BooleanField(verbose_name='Пожилой', default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'sex', 'can_help', 'need_help']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
