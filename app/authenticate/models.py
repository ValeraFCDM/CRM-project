from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from company.models import Company

class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField(verbose_name='Электронная почта', max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    is_company_owner = models.BooleanField(default=False, verbose_name='Владелец компании')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'Пользователь: {self.username} ({self.email})'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True