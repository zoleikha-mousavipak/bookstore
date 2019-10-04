from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic import TemplateView, RedirectView, ListView



app_name = "shop"

urlpatterns = [
    path('', shop_main, name='index'),
    path('books/', books, name='books'),
    path('book/<int:id>', book, name='book'),
    path('testform', test_form , name='testform'),
    path('msgtest2', msgtest2),
    path('api/authors/', api_authors),
    path('api/author/<int:pk>', api_author),
    # path('tttttttt', MyView.as_view('t')),
    # # path('vvvvvvvv', MyView.as_view('v')),
    # path('aboutus', TemplateView(template_name="about.html").as_view()),
    # # path('gotogoole', RedirectView(url="http://google.com").as_view()),
    # path('authors', List.as_view())
]


urlpatterns = format_suffix_patterns(urlpatterns)
