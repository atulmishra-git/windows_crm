from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission


class UserManager(BaseUserManager):

    def create_user_without_password(self, email, first_name, phone, username, surname=None):
        if not email:
            raise ValueError("ENTER AN EMAIL BUDDY")
        if not first_name:
            raise ValueError("I KNOW YOU HAVE A NAME")
        if not phone:
            raise ValueError("ENTER YOUR PHONE NUMBER")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            phone=phone,
            username=username,
            surname=surname if surname else ''
            )
        user.has_usable_password()
        user.is_superuser = False
        user.save()

        return user

    def create_user(self, email, first_name, phone, username, password, surname=None):
        if not email:
            raise ValueError("ENTER AN EMAIL BUDDY")
        if not first_name:
            raise ValueError("I KNOW YOU HAVE A NAME")
        if not phone:
            raise ValueError("ENTER YOUR PHONE NUMBER")
        if not password:
            raise ValueError("PASSWORD?!?!?!? HELLO??")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            phone=phone,
            username=username,
            surname=surname if surname else ''
            )
        user.set_password(password)
        user.is_superuser = False
        user.save()

        return user

    def create_superuser(self,  email, first_name, phone, username, password, surname=''):
        user = self.create_user(email, first_name, phone, username, password, surname)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user