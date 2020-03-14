from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from reservations import models as reservation_models


class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "로그인 상태로 사용할 수 없습니다")
        return redirect("core:core")


class UpperUserOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.upperuser is True

    def handle_no_permission(self):
        messages.error(self.request, "관리자 전용 기능입니다")
        return redirect("core:core")


class LenderOnlyView(UserPassesTestMixin):
    def test_func(self):
        lender = reservation_models.Reservation.get_lender_name(self)
        return self.request.user.username is lender

    def handle_no_permission(self):
        messages.error(self.request, "본인만 변경할 수 있습니다")
        return redirect("reservations:confirmreservationlist")
