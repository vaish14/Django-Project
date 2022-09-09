from django.db import models
import datetime
import decimal
from django.contrib.auth.models import User
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

    def get_category(self):
        return self.category

class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name

    def discount(self):
        discount_price = self.price - (self.price * Decimal('0.1'))
        return discount_price

class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
                    ('CG', 'Calgary'),
                    ('MR', 'Montreal'),
                    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return self.username + " " + self.last_name

    def bought_courses(self):
        return list(Order.objects.filter(student_id=self.id).values_list("course__name", flat=True))

    def interested_in_topics(self):
        return list(self.interested_in.values_list("name", flat=True))

class Order(models.Model):
    Status_Confirmation = [(0, 'Cancelled'),
                           (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=Status_Confirmation, default=1)
    order_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.student.username

    def total_cost(self):
        return self.sum1+ self.course.price

class Interest(models.Model):
    interested = models.CharField(max_length=200)
    levels = models.IntegerField(default=1)
    comments = models.CharField(max_length=200, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=20, default="", null=True)
    orders = models.ManyToManyField(Order)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, null=True)
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, null=True)