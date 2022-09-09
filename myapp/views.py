from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import InterestForm, OrderForm, LoginForm
from .models import Topic, Course, Student, Order, Interest
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import F
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.signals import user_logged_out

def do_stuff(sender, user, request, **kwargs):
    request.delete_cookie('last_login')


user_logged_out.connect(do_stuff)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                request.session['last_login'] = str(datetime.now())
                response = HttpResponseRedirect(reverse('myapp:index'))
                response.set_cookie('last_login', datetime.now() , max_age=3600)
                login(request, user)
                return response
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        context = {'form': LoginForm() }
        return render(request, 'myapp/login.html', context)

@login_required
def user_logout(request):
    #   logout(request)  # COMMENTING FOR PART 2C
    del request.session['last_login']
    response = HttpResponseRedirect(reverse('myapp:index'))
    response.delete_cookie('last_login')
    return response

@login_required
def myaccount(request):
    user = get_user(request)
    if hasattr(user, 'student'):
        student = user.student
        context = {
            'interested_in_topics': student.interested_in_topics,
            'bought_courses': student.bought_courses,
            'first_name': student.first_name,
            'last_name': student.last_name
        }
        return render(request, 'myapp/myaccount.html', context)
    else:
        msg = "You are not a registered student!"
        return render(request, 'myapp/not_student_account.html', {'msg': msg})

def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


def about(request):
    print("Welcome guys")
    return render(request, 'myapp/about.html')


def detail(request, top_no):
    response = HttpResponse()
    topics = Topic.objects.filter(id=top_no).values()
    if not topics:
        response.write(get_object_or_404(topics))
        return response

    # para = '<p> Category is:  ' + str(topics[0].get('category')) + '</p>'
    # response.write(para)
    courses = Course.objects.filter(topic=top_no)

    # response.write('<ul>')
    # for c in courses:
    # para = '<li>' + str(c) + '</li>'
    # response.write(para)
    # response.write('</ul>')
    return render(request, 'myapp/detail.html',
                  {'topic_name': topics[0].get('category'), 'name': topics[0].get('name'), 'courses': courses})
def placeorder(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                course = order.course
                if course.price > 150:
                    course.price = course.discount()
                    course.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})

def courses(request):
    course_list = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'course_list': course_list})

def coursedetail(request, course_no):
    course = get_object_or_404(Course, id=course_no)
    context = {'course': course}
    return render(request, 'myapp/coursedetail.html', context)

def add_interest(request, course_no):
    if request.method == 'POST':
        form = InterestForm(request.POST, request.FILES)
        if form.is_valid():
            interest = Interest()
            interest.interested = form.cleaned_data['interested']
            interest.levels = form.cleaned_data['levels']
            interest.comments = form.cleaned_data['comments']
            interest.save()
            course = get_object_or_404(Course, id=course_no)
            course.interested = F("interested") + 1
            course.save(update_fields=["interested"])

            return render(request, 'myapp/interest_success.html', {'msg': "Your Interest has been saved successfully."})
        else:
            context = {'form': InterestForm()}
            return render(request, 'myapp/interest.html', context)
    else:

        context = {'form': InterestForm(), 'course_id': get_object_or_404(Course, id=course_no).id}
        return render(request,'myapp/interest.html', context)


