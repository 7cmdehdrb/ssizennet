from django.db import models
from django.urls import reverse
from core import models as core_models
from django.utils import timezone
import uuid

# Create your models here.


class Reservation(core_models.TimeStampedModel):

    """ Reservation model define """

    STATUS_BEFORE = "before"
    STATUS_NOW = "now"
    STATUS_FINISH = "finish"

    STATUS_CHOICES = (
        (STATUS_BEFORE, "대여전"),
        (STATUS_NOW, "대여중"),
        (STATUS_FINISH, "반납완료"),
    )

    CATAGOTY_INFO = "info"
    CATAGOTY_SCHOOL_EVENTS = "school"
    CATAGORY_REFINE = "refine"
    CATAGOTY_REALITY = "realiy"
    CATAGORY_PERFORM = "perform"
    CATAGORY_RADIO = "radio"
    CATAGORY_SURV = "surv"
    CATAGORY_PERSONAL = "personal"

    CATAGORY_CHOICES = (
        (CATAGOTY_INFO, "정보"),
        (CATAGOTY_SCHOOL_EVENTS, "교내행사"),
        (CATAGORY_REFINE, "교양"),
        (CATAGOTY_REALITY, "예능"),
        (CATAGORY_PERFORM, "공연"),
        (CATAGORY_RADIO, "라디오"),
        (CATAGORY_SURV, "영상제"),
        (CATAGORY_PERSONAL, "개인"),
    )

    lender = models.ForeignKey(
        "users.USER", on_delete=models.CASCADE, related_name="lender"
    )
    catagory = models.CharField(
        choices=CATAGORY_CHOICES, max_length=10, default=CATAGOTY_INFO
    )
    purpose = models.CharField(max_length=30, default="")
    equipment = models.ManyToManyField("equips.Equip", related_name="equipment")
    check_in = models.DateTimeField(default=timezone.now())
    check_out = models.DateTimeField(default=timezone.now())
    status = models.CharField(
        choices=STATUS_CHOICES, default=STATUS_BEFORE, max_length=10
    )
    accept = models.BooleanField(default=False)

    instant_boolean = models.BooleanField(default=False)
    reserv_code = models.CharField(
        max_length=4, default=uuid.uuid4().hex[:4], blank=True
    )
    reserv_confirm = models.CharField(max_length=4, default="", blank=True)

    def __str__(self):
        if self.catagory == "info":
            self.catagory = "정보"
        elif self.catagory == "school":
            self.catagory = "교내행사"
        elif self.catagory == "refine":
            self.catagory = "교양"
        elif self.catagory == "realiy":
            self.catagory = "예능"
        elif self.catagory == "perform":
            self.catagory = "공연"
        elif self.catagory == "radio":
            self.catagory = "라디오"
        elif self.catagory == "surv":
            self.catagory = "영상제"
        elif self.catagory == "personal":
            self.catagory = "개인"
        else:
            pass
        return f"{self.lender} / [{self.catagory}] {self.purpose} / {self.check_in} ~ {self.check_out}"

    def get_equipments(self):
        return ",".join([str(p) for p in self.equipment.all()])

    def get_absolute_url(self):
        return reverse("reservations:reservationdetail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-check_in"]
