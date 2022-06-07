from django.shortcuts import render
from .models import *
from  ui_project.settings import WEST_BANK_URL, EAST_BANK_URL
import requests
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def homeView(request):
    if request.method == "GET":
        r = requests.get(WEST_BANK_URL + "/bank/availability")
        availability = r.json()
        context = {}
        tuitions = Tuition.objects.all()
        json_tuitions = [{"codigo": tuition.id, "semestre": tuition.semester, "monto": tuition.amount, "carrera": tuition.major} for tuition in tuitions]
        context.update({"tuitions": json_tuitions, "payment": availability["Endpoint de pago"], "balance": availability["Endpoint de balance"]})
        
        return render(request, "home.html", context=context)


def payTuitionView(request, tuition_id):
    if request.method == "GET":
        return render(request, "pago.html", context = {"id_matricula": tuition_id})
    elif request.method == "POST":
        print(request.POST)
        bank_url = WEST_BANK_URL if request.POST["method"] == "WEST BANK" else EAST_BANK_URL
        tuition = Tuition.objects.get(id = tuition_id)
        data = {
            "card_number": int(request.POST["card-number"]),
            "id_number": int(request.POST["cc"]),
            "amount": tuition.amount,
            "callback": "http://127.0.0.1:8000/callback",
            "transaction_number": tuition_id,
            "key": int(request.POST["key"])
        }
        print(data)
        r = requests.post(bank_url + "/bank/pay", json = data, data=data)
        print(r.json())
        tuition_payment = TuitionPayment(payer_name = request.POST["name"], 
            tuition = tuition, 
            email = request.POST["email"], 
            concept = request.POST["concept"], 
            sede = request.POST["sede"], 
            card_number = int(request.POST["card-number"]))

        tuition_payment.save()
        return render(request, "pago.html", context = {"id_matricula": tuition_id, "mensaje": "pago en proceso"})


@csrf_exempt
def callbackView(request):
    print("received callback")
    if request.method == "POST":
        tuition = Tuition.objects.filter(id = request.POST["transaction_number"])
        tuition_payment = TuitionPayment.objects.get(tuition = tuition)
        tuition_payment.state = "pagado"
        tuition_payment.save()
        print('finished callback')


def checkBalanceView(request):
    if request.method == "GET":
        return render(request, "saldo.html", context = {})
    elif request.method == "POST":
        number = request.POST["input-numero"]
        r = requests.get(WEST_BANK_URL + "/bank/balance/" + str(number))
        if r.status_code == 200:
            context = r.json()
            return render(request, "saldo.html", context = r.json())
        else:
            r = requests.get(EAST_BANK_URL + "/bank/balance/" + str(number))
            if r.status_code == 200:
                return render(request, "saldo.html", context = r.json())
            return render(request, "saldo.html", context = {"error": True})