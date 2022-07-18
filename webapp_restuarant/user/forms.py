from django.forms import ModelForm, FileInput, Form, CharField, PasswordInput
from .models import User, Profile
from django.core.exceptions import ValidationError


class UserDetailForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileDetailForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["address", "image", "phone"]
        widgets = {"image": FileInput()}


class UserChangePassword(Form):
    oldpassword = CharField(label="oldPassword", widget=PasswordInput)
    password1 = CharField(label="Password", widget=PasswordInput)
    password2 = CharField(label="Password confirmation", widget=PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز های عبور وارد شده یکسان نیستند")
        return password2
