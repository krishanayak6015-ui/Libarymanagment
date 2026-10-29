from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Student, Loan

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "author", "category", "isbn", "quantity")

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("full_name", "student_id", "email", "phone")

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ("book", "student", "due_date")
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["book"].queryset = Book.objects.all()
        self.fields["student"].queryset = Student.objects.all()
