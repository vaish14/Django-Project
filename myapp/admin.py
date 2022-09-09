from django.contrib import admin
from django.db import models
from .forms import *
from .models import Topic, Course, Student, Order
# Register your models here.
admin.site.register(Topic)
#admin.site.register(Course)
#admin.site.register(Student)
admin.site.register(Order)
admin.site.register(Interest)
admin.site.register(Tag)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm




