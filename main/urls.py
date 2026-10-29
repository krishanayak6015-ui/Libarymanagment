from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.LibraryLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("books/", views.books_list, name="books"),
    path("books/add/", views.book_add, name="book_add"),
    path("books/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("students/", views.students_list, name="students"),
    path("students/add/", views.student_add, name="student_add"),
    path("students/<int:pk>/edit/", views.student_edit, name="student_edit"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    path("loans/", views.loans_list, name="loans"),
    path("loans/issue/", views.loan_issue, name="loan_issue"),
    path("loans/<int:pk>/return/", views.loan_return, name="loan_return"),
]
