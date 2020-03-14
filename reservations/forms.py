from django import forms
from . import models
from equips import models as equip_models


class ReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = (
            "lender",
            "reserv_code",
            "instant_boolean",
            "check_in",
            "check_out",
            "catagory",
            "purpose",
            "equipment",
        )
        widgets = {
            "lender": forms.HiddenInput(),
            "equipment": forms.CheckboxSelectMultiple(),
            "instant_boolean": forms.HiddenInput,
            "reserv_code": forms.HiddenInput(),
        }

        labels = {
            "check_in": "대여 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "check_out": "반납 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "catagory": "구분",
            "purpose": "목적",
            "equipment": "대여 장비",
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields["equipment"].queryset = equip_models.Equip.objects.filter(
            enable=True
        )

    def save(self, *args, **kwargs):
        reservation = super().save()
        reservation.save()


class InstantReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = (
            "lender",
            "reserv_code",
            "instant_boolean",
            "check_in",
            "check_out",
            "catagory",
            "purpose",
            "equipment",
        )
        widgets = {
            "lender": forms.HiddenInput(),
            "instant_boolean": forms.HiddenInput,
            "reserv_code": forms.HiddenInput(),
            "equipment": forms.CheckboxSelectMultiple(),
        }

        labels = {
            "check_in": "대여 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "check_out": "반납 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "catagory": "구분",
            "purpose": "목적",
            "equipment": "대여 장비",
        }

    def save(self, *args, **kwargs):
        reservation = super().save()
        reservation.save()


class ReservationChangeForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = (
            "purpose",
            "accept",
            "status",
            "check_in",
            "check_out",
            "equipment",
        )
        widgets = {
            "equipment": forms.CheckboxSelectMultiple(),
        }

        labels = {
            "check_in": "변경 대여 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "check_out": "변경 반납 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "equipment": "변경 대여 장비",
        }

    def __init__(self, *args, **kwargs):
        super(ReservationChangeForm, self).__init__(*args, **kwargs)
        self.fields["equipment"].queryset = equip_models.Equip.objects.filter(
            enable=True
        )

    def save(self, *args, **kwargs):
        reservation = super().save()
        reservation.save()


class ReservationInstantChangeForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = (
            # "purpose",
            # "accept",
            # "status",
            # "check_in",
            # "check_out",
            # "equipment",
            "purpose",
            "status",
            "accept",
            "reserv_code",
            "reserv_confirm",
            "check_in",
            "check_out",
            "equipment",
        )
        widgets = {
            "equipment": forms.CheckboxSelectMultiple(),
        }

        labels = {
            "reserv_confirm": "승인코드",
            "check_in": "변경 대여 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "check_out": "변경 반납 일시 (yyyy-mm-dd hh:mm:ss 24시간 표기)",
            "equipment": "변경 대여 장비",
        }

    def __init__(self, *args, **kwargs):
        super(ReservationInstantChangeForm, self).__init__(*args, **kwargs)
        self.fields["equipment"].queryset = equip_models.Equip.objects.filter(
            enable=True
        )

    def save(self, *args, **kwargs):
        reservation = super().save()
        reservation.save()

