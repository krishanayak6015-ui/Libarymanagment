from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    category = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} — {self.author}"

    @property
    def available_quantity(self):
        active_loans = self.loans.filter(returned_at__isnull=True).count()
        return max(self.quantity - active_loans, 0)


class Student(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    student_id = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="loans")
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name="loans")
    issued_at = models.DateField(default=timezone.localdate)
    due_date = models.DateField()
    returned_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self):
        return f"{self.book.title} → {self.student.full_name}"

    @property
    def is_overdue(self):
        return self.returned_at is None and self.due_date < timezone.localdate()
