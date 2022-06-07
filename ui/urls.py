from django.urls import path, re_path
from . import views

urlpatterns = [
    path("home", views.homeView),
    path("checkBalance", views.checkBalanceView),
    re_path(r"pay/(?P<tuition_id>\d+)$", views.payTuitionView),
    path("callback", views.callbackView)
]