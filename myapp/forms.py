from django import forms
from django.contrib.auth.forms import UserCreationForm
from myapp.models import Order, Review, Student


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label='Student Name')
    length = forms.TypedChoiceField(widget=forms.RadioSelect, choices=LENGTH_CHOICES, coerce=int, required=False,
                                    label='Preferred course duration:')
    max_price = forms.IntegerField(min_value=0, label='Maximum Price')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_status': forms.RadioSelect}
        labels = {'student': u'Student Name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'course': forms.RadioSelect}
        labels = {'reviewer': u'Please enter a valid email',
                  'rating': u'Rating: An integer between 1 (worst) and 5 (best)', }


class RegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'email', 'level', 'address', 'province', 'registered_courses',
                  'interested_in']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_image']
        labels = {'student_image': 'Upload Image '}


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='User Name')

