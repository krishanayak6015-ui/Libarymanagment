from django.contrib import admin
from .models import Book, Student, Loan

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "quantity", "isbn")
    search_fields = ("title", "author", "isbn")
    list_filter = ("category",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "student_id", "email", "phone")
    search_fields = ("full_name", "student_id", "email")

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("book", "student", "issued_at", "due_date", "returned_at")
    list_filter = ("issued_at", "due_date", "returned_at")
