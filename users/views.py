from django.shortcuts import redirect, reverse, render
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:core")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        username_info = user.clean_username.__self__
        messages.add_message(self.request, messages.INFO, f"{username_info}님 어서오세요!")
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:core")


def logout_view(request):
    messages.info(request, "안녕히가세요!")
    logout(request)
    return redirect(reverse("core:core"))


class SignUpView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    # success_url = reverse_lazy("core:core")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "회원가입 완료!")
        # Put function here
        return reverse_lazy("core:core")


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UpdateProfileView(mixins.LoggedInOnlyView, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "username",
        "avatar",
        "email",
        "departure",
        "order",
        "kakaotalk",
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["username"].widget.attrs = {"placeholder": ""}
        form.fields["username"].label = "이름"
        form.fields["username"].help_text = ""
        form.fields["email"].widget.attrs = {"placeholder": ""}
        form.fields["email"].label = "이메일"
        form.fields["departure"].widget.attrs = {"placeholder": ""}
        form.fields["departure"].label = "부서"
        form.fields["order"].widget.attrs = {"placeholder": ""}
        form.fields["order"].label = "기수"
        form.fields["kakaotalk"].widget.attrs = {"placeholder": ""}
        form.fields["kakaotalk"].label = "카카오톡 ID"
        return form

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "수정 완료!")
        return self.request.user.get_absolute_url()


class UpdatePasswordView(mixins.LoggedInOnlyView, PasswordChangeView):

    model = models.User
    template_name = "users/update-password.html"
    fields = (
        "old_password",
        "new_password1",
        "new_password2",
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].label = ""
        form.fields["old_password"].widget.attrs = {"placeholder": "기본 비밀번호"}
        form.fields["new_password1"].label = ""
        form.fields["new_password1"].widget.attrs = {"placeholder": "새 비밀번호"}
        form.fields["new_password2"].label = ""
        form.fields["new_password2"].widget.attrs = {"placeholder": "새 비밀번호 확인"}
        return form

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "수정 완료!")
        return self.request.user.get_absolute_url()
