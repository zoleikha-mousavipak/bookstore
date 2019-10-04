from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import SomeForm, BookForm
from django.contrib import messages

from .serializer import *
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status


def shop_main(request):
    return render(request, 'shop/index.html')


def books(request):
    user = request.user
    if user.is_authenticated:
        all_books = Book.objects.all()
        context = {
            'books': all_books,
        }
        return render(request, 'shop/books.html', context)
    else:
        return render(request, 'shop/access_denied_error.html')


from django.contrib.auth.decorators import permission_required
from payment.models import Payment


@login_required
# @permission_required('shop.view_book', raise_exception=True, login_url="/accounts/login/")
def book(request, id):
    book = Book.objects.get(pk=id)
    if not request.user.has_perm('shop.view_book') and book.id == 5:
        pass
    p = Payment(amount=1000, user=request.user, description="Blah Blah")
    p.save()
    return p.pay()

    context = {
        'book': book,
    }
    return render(request, 'shop/book.html', context)


def sender(request):
    email = EmailMessage("Hello", 'testMessage', to=['zmpak2000@gmail.com'],
                         attachments=[open('fsdfsf')])
    email.send()


@login_required
def test_form(request):
    # print(repr(request))
    if request.method == "POST":
        # f1 = request.POST['f1']  #from htmlform
        # return HttpResponse(f1)
        f = SomeForm(request.POST)
        if f.is_valid():
            f1 = f.cleaned_data['f1']
            f2 = f.cleaned_data['f2']
            print(f)
            print(f2)

    else:
        f = SomeForm()  #from forms.py and htmlform.as..
    return render(request, 'shop/testform.html', {'form':f})


# def test_form1(request, id):
def test_form1(request):
    # b=Book.objects.get(id=id)
    if request.method == "POST":
        # f = BookForm(b, request.POST)
        f = BookForm(request.POST)
        if f.is_valid():
            f.save(commit=False)
            f.genre = 1
            f.save()
    else:
        f = BookForm()
        # f=BookForm(b)
    return render(request, 'shop/testform.html', {'form':f})


# set flash message
def msgtest2(request):
    if request.GET.get('set') is not None:
        messages.add_message(request, messages.INFO, "Test message")
        messages.add_message(request, messages.DEBUG, "Test message")
        messages.add_message(request, messages.SUCCESS, "Test message")
        messages.add_message(request, messages.WARNING, "Test message")
        messages.add_message(request, messages.ERROR, "Test message")
    return render(request, 'main.html')


# rest_api  : for Authors model

# method 1:

# @csrf_exempt
# def api_authors(request, format=None):
#     if request.method == "GET":
#         authors= Author.objects.all()
#         serializer = AuthorSerializer(authors, many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer=AuthorSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#     return JsonResponse(serializer.errors, status=400)

# method 2:

@api_view(['GET','POST'])

def api_authors(request, format=None):
    if request.method == "GET":
        authors=Author.objects.all()
        serializer=AuthorSerializer(authors,many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# detail of one Author
#
# @api_view(['GET','PUT','DELETE'])
# def api_author(request, pk, format=None):
#     try:
#         author = Author.objects.get(pk=pk)
#         # author = Author.objects.get(pk=pk , is_deleted=False)
#     except Author.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = AuthorSerializer(author)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         serializer = AuthorSerializer(author, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == "DELETE":
#         # author.is_deleted = True (soft delete)
#         author.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# @csrf_exempt
@api_view(['GET', "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def api_author(request, pk, format=None):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(author, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        author.delete()
        return HttpResponse(status=204)


# set custom error pages

def page_not_found_view(request, exception=None):
    return HttpResponse('Error handler content', status=404)


def error_view(request, exception=None):
    return HttpResponse('Error handler content', status=500)


def permission_denied_view(request, exception=None):
    return HttpResponse('Error handler content', status=403)


def bad_request_view(request, exception=None):
    return HttpResponse('Error handler content', status=400)


# Generic views(class base view)
from django.views import  View
from django.views.generic import ListView

class MyView(View):
    form = test_form
    def __init__(self, type):
        self.type = type

    def get(self, request):
        f = self.form()
        return HttpResponse("test")

    def post(self,request):
        return HttpResponse("test")


class List(ListView):
    class Meta:
        model = Author
        template = "List_author.html"