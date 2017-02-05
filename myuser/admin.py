from django import forms
from simplemathcaptcha.fields import MathCaptchaField
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import MyUser


class UserCreationForm(forms.ModelForm):
		password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
		password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm password'}))
		captcha = MathCaptchaField()
		class Meta:
			model = MyUser
			fields = ('email', 'date_of_birth')
		def __init__(self, *args, **kwargs):
				super(UserCreationForm,self).__init__(*args,**kwargs)
				self.fields['date_of_birth'].widget.attrs={'class':'form-control','placeholder':'Date of birth'}
				self.fields['email'].widget.attrs={'class':'form-control','placeholder':'Email'}
		def clean_password2(self):
			password1 = self.cleaned_data.get("password1")
			password2 = self.cleaned_data.get("password2")
			if password1 and password2 and password1 != password2:
					raise forms.ValidationError("Passwords don't match")
			return password2
		def save(self, commit=True):
			user = super(UserCreationForm, self).save(commit=False)
			user.set_password(self.cleaned_data["password1"])
			if commit:
					user.save()
			return user


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2','captcha')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
