from django.db import models
from datetime import datetime as dt
from django.core.validators import RegexValidator

# Create your models here.

from django.db import models


class Book(models.Model):
    bookID = models.IntegerField()
    title = models.CharField(max_length=200)
    authors = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    isbn = models.CharField(max_length=13)
    isbn13 = models.CharField(max_length=13)
    language_code = models.CharField(max_length=10)
    num_pages = models.PositiveIntegerField()
    ratings_count = models.PositiveIntegerField(null=True)
    text_reviews_count = models.PositiveIntegerField(null=True)
    publication_date = models.DateField(null=True, blank=True)
    publisher = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.publication_date:
            try:
                formatted_date = dt.strptime(self.publication_date, "%m/%d/%Y").date()
                self.publication_date = formatted_date
            except ValueError:
                pass  

        super().save(*args, **kwargs)


class Member(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True, error_messages={"unique": "Email id must be unique"}
    )

    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex="^\d{10}$", message="Enter a valid number")],
    )
    address = models.TextField()
    debt = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transactionID = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now=True)
    return_date = models.DateField(null=True, blank=True)
    rent_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"Transaction ID: {self.transactionID} - Member: {self.member.name} - Book: {self.book.title}"
