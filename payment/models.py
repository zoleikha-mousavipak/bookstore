from django.db import models
from accounts.models import ShopUser
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from django.conf import settings


class Payment(models.Model):
    MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    creatation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(ShopUser, on_delete=models.PROTECT)
    authority = models.CharField(max_length=255, null=True)
    refid = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, default="Pending")
    descripton = models.CharField(max_length=255, null=True)
    amount = models.IntegerField()

    def __init__(self):
        # self.client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        self.client = Client(settings.ZARINPAL.get('url'))



    def pay(self, request, callback):
        from django.urls import reverse
        # url for shaparak to comeback
        url = reverse('payment:verify', kwargs={'to': callback} if callback else None)
        # work with sop services
        result = self.client.service.Paymentequest(self.MERCHANT, self.amount, self.descripton, self.user.email, '', url)
        if request.Status == 100:
            self.authority = result.Authority
            self.save()
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
        else:
            self.status = result.Status
            self.save()
            return HttpResponse('Error code: ' + str(result.Status))

    # accourding to url = reverse ....
    def verify(self,request):
        result = self.client.service.PaymentVerification(self.MERCHANT , self.authority, self.amount)
        if result.Status == 100:
            self.refid = str(result.RefID)
            self.status = "done"
            self.save()
            return HttpResponse('Transaction success. \nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            self.status = str(result.Status)
            self.save()
            return HttpResponse('Transaction submitted: ' + str(result.Status))
        else:
            self.status = str(result.Status)
            self.save()
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))



























