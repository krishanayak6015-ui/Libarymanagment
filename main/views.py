from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import SignupForm, BookForm, StudentForm, LoanForm
from .models import Book, Student, Loan

def home(request):
    return render(request, "home.html", {
        "book_count": Book.objects.count(),
        "student_count": Student.objects.count(),
        "issued_count": Loan.objects.filter(returned_at__isnull=True).count(),
    })

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "signup.html", {"form": form})

class LibraryLoginView(LoginView):
    template_name = "login.html"
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    today = timezone.localdate()
    context = {
        "book_count": Book.objects.count(),
        "student_count": Student.objects.count(),
        "issued_count": Loan.objects.filter(returned_at__isnull=True).count(),
        "overdue_count": Loan.objects.filter(returned_at__isnull=True, due_date__lt=today).count(),
        "recent_loans": Loan.objects.select_related("book", "student")[:5],
    }
    return render(request, "dashboard.html", context)

@login_required
def books_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query) |
            Q(isbn__icontains=query)
        )
    return render(request, "books.html", {"books": books, "query": query})

@login_required
def book_add(request):
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book added successfully.")
        return redirect("books")
    return render(request, "book_form.html", {"form": form, "heading": "Add Book"})

@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book updated successfully.")
        return redirect("books")
    return render(request, "book_form.html", {"form": form, "heading": "Edit Book"})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        if book.loans.exists():
            messages.error(request, "This book has loan history and cannot be deleted. Set its quantity to 0 instead.")
            return redirect("books")
        book.delete()
        messages.success(request, "Book deleted.")
        return redirect("books")
    return render(request, "confirm_delete.html", {"object": book, "kind": "book"})

@login_required
def students_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(email__icontains=query)
        )
    return render(request, "students.html", {"students": students, "query": query})

@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student added successfully.")
        return redirect("students")
    return render(request, "student_form.html", {"form": form, "heading": "Add Student"})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully.")
        return redirect("students")
    return render(request, "student_form.html", {"form": form, "heading": "Edit Student"})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        if student.loans.exists():
            messages.error(request, "This student has loan history and cannot be deleted.")
            return redirect("students")
        student.delete()
        messages.success(request, "Student deleted.")
        return redirect("students")
    return render(request, "confirm_delete.html", {"object": student, "kind": "student"})

@login_required
def loans_list(request):
    loans = Loan.objects.select_related("book", "student").all()
    return render(request, "loans.html", {"loans": loans})

@login_required
def loan_issue(request):
    form = LoanForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        loan = form.save(commit=False)
        if loan.book.available_quantity < 1:
            form.add_error("book", "No copies of this book are currently available.")
        elif loan.due_date < timezone.localdate():
            form.add_error("due_date", "Due date cannot be in the past.")
        else:
            loan.save()
            messages.success(request, "Book issued successfully.")
            return redirect("loans")
    return render(request, "book_form.html", {"form": form, "heading": "Issue a Book"})

@login_required
def loan_return(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == "POST":
        if loan.returned_at is None:
            loan.returned_at = timezone.localdate()
            loan.save(update_fields=["returned_at"])
            messages.success(request, "Book marked as returned.")
        return redirect("loans")
    return render(request, "confirm_delete.html", {"object": loan, "kind": "return"})
