from django import forms
from django.contrib.auth import password_validation
from . import models


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            "username",
            "password",
            "re_password",
            "email",
            "departure",
            "order",
            "kakaotalk",
        )

        labels = {
            "username": "이름",
            "password": "비밀번호",
            "re_password": "비밀번호 확인",
            "email": "이메일 주소",
            "departure": "부서",
            "order": "기수",
            "kakaotalk": "카카오톡 ID",
        }

        # it depends on User model

    username = forms.CharField(widget=forms.TextInput(), label="이름")
    password = forms.CharField(widget=forms.PasswordInput(), label="비밀번호")
    re_password = forms.CharField(widget=forms.PasswordInput(), label="비밀번호 확인")

    def clean_re_password(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if password != re_password:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다")
        else:
            try:
                password_validation.validate_password(password, self.instance)

                return password
            except forms.ValidationError as error:
                self.add_error("password", error)
            return password

    def save(self, *args, **kwargs):
        user = super().save()
        password = self.cleaned_data.get("password")
        user.set_password(password)
        user.save()


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "이름"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호 오류!"))
        except models.User.DoesNotExist:
            self.add_error("username", forms.ValidationError("해당 유저가 존재하지 않습니다"))

