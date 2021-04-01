from base64 import b64decode
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from Concours.models import *
from Account.models import UserData


class Home(TemplateView):
    http_method_names = ['get', ]

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/exams/')
        ctx = dict()
        try:
            ctx['pack'] = request.session['pack']
            ctx['role'] = request.session['user_data'].role
        except KeyError:
            return HttpResponseRedirect('/pack/')
        ctx['exam'] = APOSExam.objects.filter(concours__actif=True)[0:10]
        ctx['myexam'] = APOSUserPay.objects.filter(user=request.user)
        return render(request, "Concours/index.html", context=ctx)
        pass


class Cart(TemplateView):
    http_method_names = ['get', ]

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/exams/')
        ctx = dict()
        try:
            ctx['pack'] = request.session['pack']
        except KeyError:
            return HttpResponseRedirect('/pack/')
        m = list()
        if len(request.session['cart']) > request.session['size']:
            for r in range((request.session['size'])):
                m.append(request.session['cart'][r])
        else:
            for r in (request.session['cart']):
                m.append(r)
        request.session['cart'] = m
        l = list()
        for r in request.session['cart']:
            l.append(r.id)
        ctx['exam'] = APOSExam.objects.filter(concours__actif=True).exclude(id__in=l)[0:10]
        price = 0
        total_sms = 2
        total_email = 0
        for i in range(len(request.session['cart'])):
            price += int(ctx['pack'].prix_ver) + int(ctx['pack'].prix_end) + int(ctx['pack'].prix_sms)*2 + int(ctx['pack'].prix_mail)*2
            total_sms += 2
            total_email += 2
        request.session['sms'] = total_sms
        request.session['mail'] = total_email
        ctx['total'] = price
        ctx['api'] = APOSPaymentAPI.objects.filter(status=True)
        return render(request, "Concours/cart.html", context=ctx)
        pass


def add(request, uid):
    if request.method == "POST" and not request.is_ajax():
        if not 'cart' in request.session:
            request.session['cart'] = list()
        if 'next' in request.GET:
            next = request.GET['next']
        else:
            next = '/exams/'
        n = request.session['cart']
        if len(n) >= request.session['size']:
            print(len(n))
            return HttpResponseRedirect(next + '?err=0')
        n.append(APOSExam.objects.get(id=uid))
        request.session['cart'] = n
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/exams/')
    pass


def remove(request, uid):
    if request.method == "POST" and not request.is_ajax():
        if not 'cart' in request.session:
            request.session['cart'] = list()
        n = request.session['cart']
        n.remove(APOSExam.objects.get(id=uid))
        request.session['cart'] = n
        if 'next' in request.GET:
            next = request.GET['next']
        else:
            next = '/exams/'
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect('/exams/')
    pass


class Pay(TemplateView):
    http_method_names = ['get', 'post']

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/exams/')
        if len(request.session['cart']) < request.session['min']:
            return HttpResponseRedirect('/cart/')
        ctx = dict()
        try:
            ctx['pack'] = request.session['pack']
        except KeyError:
            return HttpResponseRedirect('/pack/')
        try:
            ctx['api'] = APOSPaymentAPI.objects.get(id=request.GET['api'])
        except KeyError:
            ctx['api'] = None
        try:
            ctx['usr'] = UserData.objects.get(user_id=request.user.id)
        except UserData.DoesNotExist:
            return HttpResponseRedirect('/login/?next=/cart/')
        return render(request, "Concours/pay.html", context=ctx)
        pass

    def post(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/exams/')
        tel = request.POST['tel']
        p = APOSUserPay.objects.create(
            user=request.user,
            status=True, stat=request.session['role'],
            pack=request.session['pack'],
            rest_sms=request.session['sms'],
            rest_mail=request.session['mail']
        )
        p.exams.set(request.session['cart'])
        f = APOSReceipt(
            pid_id=p.uid, pay_id=request.POST['api'], number=tel
        )
        p.save()
        f.save()
        del request.session['pack']
        del request.session['min']
        del request.session['cart']
        del request.session['size']
        del request.session['sms']
        del request.session['mail']
        return HttpResponseRedirect('/receipt/' + str(p.uid) + '/')
        pass


class Service(TemplateView):
    http_method_names = ['get', 'post']

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/exams/')
        if len(request.session['cart']) < request.session['min']:
            return HttpResponseRedirect('/cart/')
        ctx = dict()
        try:
            ctx['pack'] = request.session['pack']
        except KeyError:
            return HttpResponseRedirect('/pack/')
        ctx['api'] = APOSPaymentAPI.objects.filter(status=True)
        return render(request, "Concours/service.html", context=ctx)
        pass


class Pack(TemplateView):
    http_method_names = ['get', 'post']

    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/login/?next=/pack/')
        try:
            t = request.GET['change']
            if int(t) == 0:
                del request.session['pack']
                del request.session['size']
                return HttpResponseRedirect('/pack/')
            else:
                pass
        except KeyError:
            pass
        except ValueError:
            pass
        ctx = dict()
        ctx['api'] = APOSPrice.objects.filter()
        return render(request, "Concours/pack.html", context=ctx)
        pass

    def post(self, request, **kwargs):
        request.session['pack'] = APOSPrice.objects.get(pk=request.POST['pack'])
        request.session['size'] = APOSPrice.objects.get(pk=request.POST['pack']).max_val
        request.session['min'] = APOSPrice.objects.get(pk=request.POST['pack']).min_val
        try:
            next = request.POST['next']
        except KeyError:
            try:
                next = request.GET['next']
            except KeyError:
                next = '/exams/'
        return HttpResponseRedirect(next)
        pass


def receipt(request, id):
    return render(request, "Concours/receipt.html", context=None)
