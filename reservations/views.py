from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView, DetailView, DeleteView
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.forms.models import modelform_factory
from django.forms import CheckboxSelectMultiple, ModelMultipleChoiceField
from . import forms, models
from users import mixins as user_mixins
from equips import models as equip_models
import datetime
from teleg import send_text, send_admin


# Create your views here.
# lender = user_models.objects.get(user=request.user)


""" 기본 예약 """


class MakeReservationView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "reservations/makereservation.html"
    form_class = forms.ReservationForm

    def form_valid(self, form):
        lender = form.cleaned_data.get("lender")
        catagory = form.cleaned_data.get("catagory")
        if catagory == "info":
            catagory = "정보"
        elif catagory == "school":
            catagory = "교내행사"
        elif catagory == "refine":
            catagory = "교양"
        elif catagory == "realiy":
            catagory = "예능"
        elif catagory == "perform":
            catagory = "공연"
        elif catagory == "radio":
            catagory = "라디오"
        elif catagory == "surv":
            catagory = "영상제"
        elif catagory == "personal":
            catagory = "개인"
        else:
            pass
        purpose = form.cleaned_data.get("purpose")
        check_in = form.cleaned_data.get("check_in")
        check_out = form.cleaned_data.get("check_out")
        reserv_code = form.cleaned_data.get("reserv_code")

        now = timezone.now()
        now_day = now.day
        check_in_day = check_in.day

        """ time zone """

        """ / 중복처리 """

        def check_double():
            count = 0
            equips = form.cleaned_data.get("equipment")
            # ㄴ 내가 빌린 장비
            check_in = form.cleaned_data.get("check_in")
            check_out = form.cleaned_data.get("check_out")
            equipment = models.Reservation.objects.values()
            #  ㄴ 모든 빌려있는 장비
            for equip in equips:
                for check in equipment:
                    data = (
                        models.Reservation.objects.filter(
                            check_in__range=(check_in, check_out)
                        )
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data:
                        count = count + 1

                    data2 = (
                        models.Reservation.objects.filter(
                            check_out__range=(check_in, check_out)
                        )
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data2:
                        count = count + 1

            if count != 0:
                return False
            else:
                return True

        """ 중복처리 / """

        if now_day == check_in_day:
            messages.add_message(self.request, messages.ERROR, "당일대여가 필요합니다!")
            return redirect(reverse("reservations:instantreservation"))
        elif check_in >= check_out or check_in < now:
            messages.add_message(self.request, messages.ERROR, "시간오류")
            return redirect(reverse("reservations:makereservation"))
        elif check_double() is False:
            messages.add_message(self.request, messages.ERROR, "이미 예약중인 장비가 있습니다")
            return redirect(reverse("reservations:makereservation"))
        else:
            messages.add_message(self.request, messages.INFO, "예약 완료!")
            send_text(
                f"<<신청>>\n{lender} / [{catagory}] {purpose} / {check_in} ~ {check_out}"
            )
            send_admin(
                f"<<신청>>\n{lender} / [{catagory}] {purpose} / {check_in} ~ {check_out}\n[승인코드]: {reserv_code}"
            )
            form.save()
            return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse_lazy("core:core")

    def get_initial(self):
        initial = super().get_initial()
        initial["lender"] = self.request.user
        initial["instant_boolean"] = False
        return initial


""" 예약 목록 """


class ReservationListView(ListView):
    def get(self, request):

        now = timezone.now()
        now_day = now.day
        before_1h = now - datetime.timedelta(hours=1)
        after_1h = now + datetime.timedelta(hours=1)

        """ time zone """

        qs = models.Reservation.objects.all()
        paginator = Paginator(qs, 10)
        page = request.GET.get("page", 1)
        reservations = paginator.get_page(page)
        get_copy = request.GET.copy()
        address = get_copy.pop("page", True) and get_copy.urlencode()
        return render(
            request,
            "reservations/list.html",
            {
                "reservations": reservations,
                "address": address,
                "now": now,
                "now_day": now_day,
                "before_1h": before_1h,
                "after_1h": after_1h,
            },
        )


class ConfirmRevervationListView(ListView):
    def get(self, request):

        qs = models.Reservation.objects.all()
        paginator = Paginator(qs, 10)
        page = request.GET.get("page", 1)
        reservations = paginator.get_page(page)
        get_copy = request.GET.copy()
        address = get_copy.pop("page", True) and get_copy.urlencode()
        return render(
            request,
            "reservations/confirmlist.html",
            {"reservations": reservations, "address": address},
        )


""" pk 부여용 """


class ReservationDetailView(DetailView):

    model = models.Reservation
    context_object_name = "reserv_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


""" 예약 승인 """


class UpdateAcceptView(user_mixins.UpperUserOnlyView, UpdateView):

    model = models.Reservation
    template_name = "reservations/update-acception.html"
    fields = ("accept",)

    def form_valid(self, form):
        accept = form.cleaned_data.get("accept")
        if accept is True:
            msg = "승인"
        else:
            msg = "거부"
        info = self.object
        send_text(f"<<{msg}>>\n{info}")
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "승인완료!")
        return reverse("reservations:reservationlist")


""" 대여중 변환 """


class UpdateReservationNowView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Reservation
    template_name = "reservations/update-reservation-from-before-to-now.html"
    fields = ("status",)

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial["status"] = models.Reservation.STATUS_NOW
        return initial

    def form_valid(self, form):
        info = self.object
        send_text(f"<<대여>>\n{info}")
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "대여 처리 완료!")
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("reservations:reservationlist")


""" 반납 변환 """


class UpdateReservationFinishView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Reservation
    template_name = "reservations/update-reservation-from-now-to-finish.html"
    fields = ("status", "check_out")

    def get_initial(self):
        initial = super().get_initial()
        initial["status"] = models.Reservation.STATUS_FINISH
        return initial

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "반납 처리 완료!")
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("reservations:reservationlist")

    def form_valid(self, form):

        now = timezone.now()

        """ time zone """

        check_out = form.cleaned_data.get("check_out")
        gap = now - check_out

        totalsec = gap.total_seconds()
        h = int(totalsec // 3600)
        m = int((totalsec % 3600) // 60)
        info = self.object

        if now > (check_out + datetime.timedelta(hours=1)):
            send_admin(f"<<반납연체>>\n{info}\nALERT: {h}시간 {m}분 연체")
            send_text(f"<<반납>>\n{info}\n")
            return super().form_valid(form)
        else:
            send_text(f"<<반납>>\n{info}")
            return super().form_valid(form)


""" 기본 수정 """


class ReservationChangeView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Reservation
    template_name = "reservations/reservation_change.html"
    # fields = (
    #     "purpose",
    #     "accept",
    #     "status",
    #     "check_in",
    #     "check_out",
    #     "equipment",
    # )

    form_class = forms.ReservationChangeForm

    def form_valid(self, form):

        info = self.object
        purpose = form.cleaned_data.get("purpose")
        status = form.cleaned_data.get("status")
        check_in = form.cleaned_data.get("check_in")
        check_out = form.cleaned_data.get("check_out")

        now = timezone.now()
        now_day = now.day
        check_in_day = check_in.day

        """ / 중복처리 """

        def check_double():
            count = 0
            equips = form.cleaned_data.get("equipment")
            equipment = models.Reservation.objects.values()
            for equip in equips:
                for check in equipment:
                    data = (
                        models.Reservation.objects.exclude(purpose=purpose)
                        .filter(check_in__range=(check_in, check_out))
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data:
                        count = count + 1

                    data2 = (
                        models.Reservation.objects.exclude(purpose=purpose)
                        .filter(check_out__range=(check_in, check_out))
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data2:
                        count = count + 1

            if count != 0:
                return False
            else:
                return True

        """ 중복처리 / """

        if not check_double():
            messages.add_message(self.request, messages.ERROR, "이미 대여중인 장비가 있습니다")
            return redirect(reverse("reservations:reservationlist"))
        elif now_day == check_in_day or status != models.Reservation.STATUS_BEFORE:
            messages.add_message(self.request, messages.ERROR, "당일에는 당일 연장만 가능합니다")
            return redirect(reverse("reservations:reservationlist"))
        else:
            messages.add_message(self.request, messages.INFO, "수정 완료!")
            send_text(f"<<수정>>\n{info}\n")
            return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("reservations:reservationlist")

    def get_initial(self):
        initial = super().get_initial()
        initial["accept"] = False
        initial["status"] = models.Reservation.STATUS_BEFORE
        return initial


""" 당일 예약 """


class InstantReservationView(user_mixins.LoggedInOnlyView, FormView):

    template_name = "reservations/instantreservation.html"
    form_class = forms.InstantReservationForm

    def form_valid(self, form):

        lender = form.cleaned_data.get("lender")
        catagory = form.cleaned_data.get("catagory")
        if catagory == "info":
            catagory = "정보"
        elif catagory == "school":
            catagory = "교내행사"
        elif catagory == "refine":
            catagory = "교양"
        elif catagory == "realiy":
            catagory = "예능"
        elif catagory == "perform":
            catagory = "공연"
        elif catagory == "radio":
            catagory = "라디오"
        elif catagory == "surv":
            catagory = "영상제"
        elif catagory == "personal":
            catagory = "개인"
        else:
            pass
        purpose = form.cleaned_data.get("purpose")
        check_in = form.cleaned_data.get("check_in")
        check_out = form.cleaned_data.get("check_out")
        reserv_code = form.cleaned_data.get("reserv_code")

        now = timezone.now()
        now_day = now.day
        check_in_day = check_in.day

        """ time zone """

        """ / 중복처리 """

        def check_double():
            count = 0
            equips = form.cleaned_data.get("equipment")
            check_in = form.cleaned_data.get("check_in")
            check_out = form.cleaned_data.get("check_out")
            equipment = models.Reservation.objects.values()
            for equip in equips:
                for check in equipment:
                    data = (
                        models.Reservation.objects.exclude(purpose=purpose)
                        .filter(check_in__range=(check_in, check_out))
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data:
                        count = count + 1

                    data2 = (
                        models.Reservation.objects.exclude(purpose=purpose)
                        .filter(check_out__range=(check_in, check_out))
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data2:
                        count = count + 1

            if count != 0:
                return False

            else:
                return True

        """ 중복처리 / """

        if now_day == check_in_day:
            if check_in > check_out:
                messages.add_message(self.request, messages.ERROR, "시간오류")
                return redirect(reverse("reservations:instantreservation"))
            elif check_double() is False:
                messages.add_message(
                    self.request, messages.ERROR, "이미 예약중인 장비가 있습니다",
                )
                return redirect(reverse("reservations:instantreservation"))
            else:
                messages.add_message(self.request, messages.INFO, "신청 완료! 코드를 입력해주세요")
                send_text(
                    f"<<당일신청>>\n{lender} / [{catagory}] {purpose} / {check_in} ~ {check_out}"
                )
                send_admin(
                    f"<<당일신청>>\n{lender} / [{catagory}] {purpose} / {check_in} ~ {check_out}\n[승인코드]: {reserv_code}"
                )
                form.save()
                return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.ERROR, "당일 대여가 아닙니다")
            return redirect(reverse("core:core"))

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse_lazy("core:core")

    def get_initial(self):
        initial = super().get_initial()
        initial["lender"] = self.request.user
        initial["instant_boolean"] = True
        return initial


""" 당일대여 승낙 """


class InstantReservationConfirmView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Reservation
    template_name = "reservations/confirm-instant-reservation.html"
    fields = (
        "accept",
        "instant_boolean",
        "reserv_code",
        "reserv_confirm",
    )

    def get_initial(self):
        initial = super().get_initial()
        initial["instant_boolean"] = False
        initial["accept"] = True
        initial["reserv_confirm"] = ""
        return initial

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, "코드 확인 완료!")
        return reverse("reservations:reservationlist")

    def form_valid(self, form):
        reserv_code = form.cleaned_data.get("reserv_code")
        reserv_confirm = form.cleaned_data.get("reserv_confirm")
        if reserv_code == reserv_confirm:
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.ERROR, "코드 에러!")
            return redirect(reverse("reservations:confirmreservationlist"))


""" 당일 변경 """


class InstantReservationChangeView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Reservation
    template_name = "reservations/instant_change.html"
    # fields = (
    #     "purpose",
    #     "status",
    #     "accept",
    #     "reserv_code",
    #     "reserv_confirm",
    #     "check_in",
    #     "check_out",
    #     "equipment",
    # )

    form_class = forms.ReservationInstantChangeForm

    def form_valid(self, form):

        info = self.object
        purpose = form.cleaned_data.get("purpose")
        check_in = form.cleaned_data.get("check_in")
        check_out = form.cleaned_data.get("check_out")
        reserv_code = form.cleaned_data.get("reserv_code")
        reserv_confirm = form.cleaned_data.get("reserv_confirm")
        status = form.cleaned_data.get("status")
        accept = form.cleaned_data.get("accept")

        print(accept)

        now = timezone.now()
        now_day = now.day
        check_in_day = check_in.day

        """ / 중복처리 """

        def check_double():
            count = 0
            equips = form.cleaned_data.get("equipment")
            equipment = models.Reservation.objects.values()
            for equip in equips:
                for check in equipment:
                    data = (
                        models.Reservation.objects.exclude(purpose=purpose)
                        .filter(check_in__range=(check_in, check_out))
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data:
                        count = count + 1

                    data2 = (
                        models.Reservation.objects.exclude(purpose=purpose)
                        .filter(check_out__range=(check_in, check_out))
                        .filter(equipment__name=equip)
                        .values()
                    )

                    if data2:
                        count = count + 1

            if count != 0:
                return False
            else:
                return True

        """ 중복처리 / """
        if not accept:
            messages.add_message(self.request, messages.ERROR, "승인 받지 않은 내역입니다")
            return redirect(reverse("reservations:reservationlist"))
        elif not check_double():
            messages.add_message(self.request, messages.ERROR, "이미 대여중인 장비가 있습니다")
            return redirect(reverse("reservations:reservationlist"))
        elif now_day != check_in_day:
            messages.add_message(self.request, messages.ERROR, "당일변경이 아닙니다")
            return redirect(reverse("reservations:reservationlist"))
        elif reserv_code != reserv_confirm:
            messages.add_message(self.request, messages.ERROR, "코드가 일치하지 않습니다!")
            return redirect(reverse("reservations:reservationlist"))
        elif check_double and status != models.Reservation.STATUS_FINISH:
            messages.add_message(self.request, messages.INFO, "수정 완료!")
            send_text(f"<<당일변경>>\n{info}\n")
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.ERROR, "알 수 없는 에러")
            return redirect(reverse("reservations:reservationlist"))

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("reservations:reservationlist")

    def get_initial(self):
        initial = super().get_initial()
        initial["reserv_confirm"] = ""
        return initial


""" 취소 """


class ReservationDeleteView(user_mixins.LoggedInOnlyView, DeleteView):
    model = models.Reservation
    template_name = "reservations/delete.html"
    success_url = reverse_lazy("reservations:reservationlist")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ReservationDeleteView, self).get_object()
        return obj

    def get_success_url(self):
        if self.success_url:
            info = self.object
            send_text(f"<<취소>>\n{info}")
            return self.success_url.format(**self.object.__dict__)
