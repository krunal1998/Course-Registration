from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404
from .forms import SearchForm, OrderForm, ReviewForm, RegisterForm, ImageUploadForm, ForgotPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.core.mail import send_mail


# Create your views here.
"""
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    if 'last_login' in request.session:
        last_login_time = request.session['last_login']
        return render(request, 'myapp/index.html', {'top_list': top_list, 'lastLogin':last_login_time,
                                                    'first_name':request.user.first_name})
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})

    # return render(request, 'myapp/index0.html', {'top_list': top_list})
"""
class Index(View):
    def get(self, request):
        top_list = Topic.objects.all().order_by('id')[:10]
        if 'last_login' in request.session:
            last_login_time = request.session['last_login']
            return render(request, 'myapp/index.html', {'top_list': top_list, 'lastLogin': last_login_time,
                                                        'first_name': request.user.first_name})
        else:
            error_message = "Your Last Login Was more than One Hour Ago, Please log in."
            return render(request, 'myapp/error_message.html', {'error_message': error_message})


# About page view
def about(request):
    if 'last_login' in request.session:
        if 'about_visits' in request.COOKIES:
            num_of_visits = int(request.COOKIES['about_visits'])
            num_of_visits += 1
        else:
            num_of_visits = 1
        response = render(request, 'myapp/about.html', {'total_visits': num_of_visits,
                                                        'lastLogin': request.session['last_login'],
                                                        'first_name': request.user.first_name})
        response.set_cookie('about_visits', num_of_visits, max_age=300)
        return response
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})

"""
def detail(request, topic_id):
    #    topic = Topic.objects.get(id=topic_id)
    if 'last_login' in request.session:
        topic = get_object_or_404(Topic, id=topic_id)

        course_list = Course.objects.filter(topic=topic)
        return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': course_list,
                                                     'lastLogin': request.session['last_login'],
                                                     'first_name': request.user.first_name
                                                     })
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})
"""


class Detail(View):
    def get(self, request, topic_id):
        if 'last_login' in request.session:
            topic = get_object_or_404(Topic, id=topic_id)

            course_list = Course.objects.filter(topic=topic)
            return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': course_list,
                                                         'lastLogin': request.session['last_login'],
                                                         'first_name': request.user.first_name
                                                         })
        else:
            error_message = "Your Last Login Was more than One Hour Ago, Please log in."
            return render(request, 'myapp/error_message.html', {'error_message': error_message})


def findcourses(request):
    if 'last_login' in request.session:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                length = form.cleaned_data['length']
                max_price = form.cleaned_data['max_price']

                if length:
                    topics = Topic.objects.filter(length=length)
                    courselist = []
                    for top in topics:
                        courselist = courselist + list(top.courses.filter(price__lte=max_price))
                    return render(request, 'myapp/results.html', {'courselist': courselist,
                                                                  'lastLogin': request.session['last_login'],
                                                                  'first_name': request.user.first_name
                                                                  })
                else:
                    courselist = list(Course.objects.filter(price__lte=max_price))
                    return render(request, 'myapp/results.html', {'courselist': courselist,
                                                                  'lastLogin': request.session['last_login'],
                                                                  'first_name': request.user.first_name
                                                                  })
            else:
                message = "Invalid Data!"
                return render(request, 'myapp/results.html', {'message':message,
                                                              'lastLogin': request.session['last_login'],
                                                              'first_name': request.user.first_name
                                                              })
        else:
            form = SearchForm()
            return render(request, 'myapp/findcourses.html', {'form': form,
                                                              'lastLogin': request.session['last_login'],
                                                              'first_name': request.user.first_name
                                                              })
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})


def place_order(request):
    if 'last_login' in request.session:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                courses = form.cleaned_data['courses']
                order = form.save(commit=False)
                student = order.student
                status = order.order_status
                order.save()

                if status == 1:
                    for c in order.courses.all():
                        student.registered_courses.add(c)
                    form.save()
                    return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order,
                                                                         'lastLogin': request.session['last_login'],
                                                                         'first_name': request.user.first_name
                                                                         })
            else:
                return render(request, 'myapp/place_order.html', {'form': form,
                                                                  'lastLogin': request.session['last_login'],
                                                                  'first_name': request.user.first_name
                                                                  })
        else:
            form = OrderForm()
            return render(request, 'myapp/place_order.html', {'form': form,
                                                              'lastLogin': request.session['last_login'],
                                                              'first_name': request.user.first_name
                                                              })
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['registered_courses']
            topics = form.cleaned_data['interested_in']

            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password1'])

            student.save()
            rg = student.registered_courses
            it = student.interested_in
            for t in topics:
                it.add(t)

            for c in courses:
                rg.add(c)

            form.save()
            return redirect(request, 'myapp/login.html')
        else:
            return render(request, 'myapp/register.html', {'form':form})
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form})


def review(request):
    if 'last_login' in request.session:
        try:
            currentUser = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            currentUser = None
        if currentUser and (currentUser.level == 'UG' or currentUser.level == 'PG'):
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    rating = form.cleaned_data['rating']
                    if (rating >= 1 and rating <= 5):
                        review = form.save()
                        course = Course.objects.get(id=review.course.id)
                        course.num_reviews += 1
                        course.save()
                        return redirect('myapp:index')
                    else:
                        form.add_error('rating', 'You must enter a rating between 1 and 5!')
                        return render(request, 'myapp/review.html', {'form': form,
                                                                     'lastLogin': request.session['last_login'],
                                                                     'first_name': request.user.first_name
                                                                     })
                else:
                    return render(request, 'myapp/review.html', {'form': form,
                                                                 'lastLogin': request.session['last_login'],
                                                                 'first_name': request.user.first_name
                                                                 })
            else:
                form = ReviewForm()
                return render(request, 'myapp/review.html', {'form': form,
                                                             'lastLogin': request.session['last_login'],
                                                             'first_name': request.user.first_name
                                                             })
        else:
            message = "Sorry only either Undergraduate students or Past graduates students can review."
            return render(request, 'myapp/review.html', {'message':message,
                                                         'lastLogin': request.session['last_login'],
                                                         'first_name': request.user.first_name
                                                         })
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})


def user_login(request):
    redirect_to = request.GET.get('next', '')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # set 'last_login' session object
                currentTime = datetime.now()
                request.session['last_login'] = str(currentTime)[:-7]
                # expire session after 1 hour of inactivity
                request.session.set_expiry(3600)
                return HttpResponseRedirect(redirect_to)
            else:
                error_message = 'Your account is disabled.'
                if redirect_to == '':
                    redirect_to = '/myapp'
                return render(request, 'myapp/login.html', {'redirect_to': redirect_to,
                                                            'error_message':error_message})
        else:
            error_message = 'Invalid login details.'
            if redirect_to == '':
                redirect_to = '/myapp'
            return render(request, 'myapp/login.html', {'redirect_to': redirect_to,
                                                        'error_message': error_message})
    else:
        # set redirect_to to the index page when user try to login via login link
        if redirect_to == '':
            redirect_to = '/myapp'
        return render(request, 'myapp/login.html',{'redirect_to':redirect_to})


@login_required
def user_logout(request):
    logout(request)
    error_message = "You are Logged Out."
    return render(request, 'myapp/error_message.html', {'error_message': error_message})


@login_required(login_url='/myapp/login')
def myaccount(request):
    if 'last_login' in request.session:
        try:
            currentUser = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            currentUser = None

        if currentUser:
            registeredCourses = currentUser.registered_courses.all()
            interestedtopics = currentUser.interested_in.all()
            student_image = currentUser.student_image
            # If upload image is button pressed
            if request.method == 'POST':
                form = ImageUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    currentUser.student_image = form.cleaned_data.get('student_image')
                    currentUser.save()
                    student_image = currentUser.student_image
                    return render(request, 'myapp/myaccount.html',
                                  {'first_name': currentUser.first_name, 'last_name': currentUser.last_name,
                                   'interestedTopics': interestedtopics, 'registeredCourses': registeredCourses,
                                   'student_image': student_image,
                                   'lastLogin': request.session['last_login'], 'form': form})
            # otherwise normal view
            else:
                form = ImageUploadForm()
                if student_image:
                    return render(request, 'myapp/myaccount.html',
                              {'first_name': currentUser.first_name, 'last_name': currentUser.last_name,
                               'interestedTopics': interestedtopics, 'registeredCourses': registeredCourses,
                               'student_image': student_image,
                               'lastLogin': request.session['last_login'], 'form': form})
                else:
                    return render(request, 'myapp/myaccount.html',
                                  {'first_name': currentUser.first_name, 'last_name': currentUser.last_name,
                                   'interestedTopics': interestedtopics, 'registeredCourses': registeredCourses,
                                   'lastLogin': request.session['last_login'], 'form': form})
        else:
            message = "You Are Not Registered Student. Only registered students can see this."
            return render(request, 'myapp/myaccount.html',{'message':message,
                                                           'lastLogin': request.session['last_login']})
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})


def myorders(request):
    if 'last_login' in request.session:
        try:
            currentUser = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            currentUser = None

        if currentUser:
            orders = Order.objects.filter(student=currentUser).all()
            if orders:
                coursesInOrder = [o.courses.all() for o in orders]
                odate = orders.values_list('order_date', flat=True)
                status = orders.values_list('order_status', flat=True)

                iterableOrders = zip(coursesInOrder, odate, status)

                return render(request, 'myapp/myorders.html', {'orders':iterableOrders,
                                                               'lastLogin': request.session['last_login'],
                                                               'first_name': request.user.first_name
                                                               })
            else:
                message = "You don't have any orders!"
                return render(request, 'myapp/myorders.html', {'message':message,
                                                               'lastLogin': request.session['last_login'],
                                                               'first_name': request.user.first_name
                                                               })
        else:
            message = "You Are Not Registered Student"
            return render(request, 'myapp/myorders.html', {'message': message,
                                                           'lastLogin': request.session['last_login'],
                                                           'first_name': request.user.first_name
                                                           })
    else:
        error_message = "Your Last Login Was more than One Hour Ago, Please log in."
        return render(request, 'myapp/error_message.html', {'error_message': error_message})


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                student = Student.objects.get(username=username)
                new_pwd = student.username + "1234"
                student.set_password(new_pwd)
                student.save()
                send_from = 'katrodiya80@gmail.com'
                sent_to = student.email
                mail_content = "Your new password is: " + new_pwd
                send_mail('New Password', mail_content, send_from, [sent_to])

                success_message = "New password sent to your email id."
                return render(request, 'myapp/forgot_password.html', {'form': form,
                                                                      'success_message': success_message})
            except Student.DoesNotExist:
                form= ForgotPasswordForm()
                error_message = 'Invalid Username, Try Again.'
                return render(request, 'myapp/forgot_password.html', {'form': form,
                                                                      'error_message': error_message})
    else:
        form = ForgotPasswordForm()
        return render(request, 'myapp/forgot_password.html', {'form': form})