from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser

class MyUserManager(BaseUserManager):
		def create_user(self,email,date_of_birth,password=None):
				if not email:
						raise ValueError('Email must be set')
				user=self.model(email=email,date_of_birth=date_of_birth)
				user.set_password(password)
				user.save(using=self._db)
				return user
		def create_superuser(self,email,date_of_birth,password):
				user=self.create_user(email,date_of_birth=date_of_birth,password=password)
				user.is_admin=True
				user.save(using=self._db)
				return user

class MyUser(AbstractBaseUser):
		email=models.EmailField(unique=True)
		date_of_birth=models.DateField()
		is_active=models.BooleanField(default=True)
		is_admin=models.BooleanField(default=False)
		
		objects=MyUserManager

		USERNAME_FIELD="email"
		
		REQUIRED_FIELDS=['date_of_birth']

		def get_short_name(self):
				return self.email

		def get_full_name(self):
				return self.email
		
		def  has_perms(self,perm,ob=None):
				return True

		def has_module_perms(self,app_label):
				return True

		@property
		def is_staff(self):
				self.is_admin



