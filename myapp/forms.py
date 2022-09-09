from django import forms
from myapp.models import Order, Course, Topic, Student
import datetime
from django.forms import ModelForm, RadioSelect, SelectDateWidget
from django.core.validators import MinValueValidator

from .models import *

class StudentForm(forms.ModelForm):
    interested_in = forms.ModelMultipleChoiceField(queryset=Topic.objects.all(), widget=forms.CheckboxSelectMultiple())


class InterestForm(forms.Form):
    choice = [('1', 'Yes'), ('0', 'No')]
    interested = forms.CharField(label='Interested', widget=forms.RadioSelect(choices=choice))
    levels = forms.IntegerField(min_value=1, max_value=10)
    comments = forms.CharField(label='Additional Comments', widget=forms.Textarea(), required=False)

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('student', 'course', 'levels', 'order_date')
        widgets = {
            'student': RadioSelect(),
            'order_date': SelectDateWidget()
        }
class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())