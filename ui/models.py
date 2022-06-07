from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100, default = "John Doe")
    code = models.IntegerField(primary_key=True, auto_created=True, default=1)

class Tuition(models.Model):
    amount = models.IntegerField()
    semester = models.IntegerField()
    major = models.CharField(max_length=10)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)


class TuitionPayment(models.Model):
    tuition = models.ForeignKey(Tuition, on_delete=models.PROTECT)
    date_payed = models.DateTimeField(auto_now_add=True)
    payer_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    concept = models.CharField(max_length=50)
    method = models.CharField(max_length=50)
    sede = models.CharField(max_length=50)
    card_number = models.IntegerField(max_length=50)
    state = models.CharField(max_length=20, default="creado")

