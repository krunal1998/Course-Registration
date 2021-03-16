# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('50.0')),
                                                                             MaxValueValidator(Decimal('500.0'))])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('ND', 'No Degree'),
    ]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True)
    province=models.CharField(max_length=2 , default='ON')
    registered_courses = models.ManyToManyField(Course, blank=True, null=True)
    interested_in = models.ManyToManyField(Topic)
    student_image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name + self.last_name}'


class Order(models.Model):
    OSTATUS_CHOICES = [
        (0, 'Cancelled'),
        (1, 'Confirmed'),
        (2, 'On Hold')
    ]
    courses = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=OSTATUS_CHOICES, default=1)
    order_date = models.DateField(default= timezone.now())

    def __str__(self):
        return f'{self.student.first_name, self.student.last_name, self.order_date.ctime()}'

    def total_cost(self):
        return sum([ course.price for course in self.courses.all()])

    def total_items(self):
        return self.courses.all().count()


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.course.title,"-", self.reviewer}'
