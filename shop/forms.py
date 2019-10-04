from django import forms
from bootstrap_datepicker_plus import  DatePickerInput
from .models import Book
class SomeForm(forms.Form):
    f1 = forms.CharField(label="F1:", max_length=20)
    f2 = forms.DateField(label="F2:")
    f3 = forms.DateField(label="F3:",widget=DatePickerInput(format='%m/%d/%Y'))


class BookForm(forms.ModelForm):

    # def clean(self):
    #     super().clean()

    class Meta:
        model=Book
        fields = ['title','author']