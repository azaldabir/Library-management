from django.shortcuts import render, redirect
from .models import Member, Book, Transaction
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError


def book_list(request):
    books = Book.objects.all()

    search_query = request.GET.get('search_query')

    if search_query:
        books = books.filter(title__icontains=search_query) | books.filter(authors__icontains=search_query)

    try:
        return render(request, 'book_list.html', {'books': books, 'search_query': search_query})
    except Exception as ep:
        print('Error in view:', ep)
        messages.error(request, 'An error occurred while fetching book data.')
        return redirect('book-list')


def book_create(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        title = request.POST['title']
        authors = request.POST['authors']
        language_code = request.POST['language_code']
        isbn = request.POST['isbn']
        average_rating = request.POST['average_rating']
        publication_date = request.POST['publication_date']
        publisher = request.POST['publisher']
        num_pages = request.POST['num_pages']

        book = Book(
            bookID=book_id,
            title=title,
            authors=authors,
            average_rating=average_rating,
            isbn=isbn,
            language_code=language_code,
            num_pages=num_pages,
            publication_date=publication_date,
            publisher=publisher,
        )
        book.save()

        messages.success(request, 'Book created successfully.')

        return redirect('book-list')

    return render(request, "add_book.html")

def delete_book(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect("book-list")

def update_book(request, book_id):
    book = Book.objects.get( bookID=book_id)

    if request.method == 'POST':
        book.bookID = request.POST['bookID']
        book.title = request.POST['title']
        book.authors = request.POST['authors']
        book.average_rating = request.POST['average_rating']
        book.isbn = request.POST['isbn']
        book.isbn13 = request.POST['isbn13']
        book.language_code = request.POST['language_code']
        book.num_pages = request.POST['num_pages']
        book.ratings_count = request.POST['ratings_count']
        book.text_reviews_count = request.POST['text_reviews_count']
        book.publication_date = request.POST['publication_date']
        book.publisher = request.POST['publisher']

        book.save()

        messages.success(request, 'Book updated successfully.')

        return redirect('book-list')

    return render(request, 'update_book.html', {'book': book})

def members(request):
    members = Member.objects.all()
    return render(request, "members.html", {"members": members})

def create_member(request):
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            address = request.POST.get("address")

            member = Member(
                name=name,
                email=email,
                phone=phone,
                address=address
            )
            member.full_clean()  
            member.save()
            messages.success(request, 'Member created successfully.')
            return redirect("member")

        return render(request, "add_member.html")
    
    except ValidationError as error_msgs:
        print(">>", error_msgs)
        for key, msg in error_msgs:
            messages.error(request, msg[0])
            return redirect("add-member")
        
    except Exception as ep:
        messages.error(request, ep)
        return redirect("member")

def update_member(request, memberID):
    member = Member.objects.filter( id=memberID)

    if request.method == 'POST':
        member.name = request.POST['name']
        member.email = request.POST['email']
        member.phone = request.POST['phone']

        member.save()

        messages.success(request, 'Member updated successfully.')

        return redirect('member')

    return render(request, 'update_member.html', {'member': member})

def delete_member(request, memberID):
    member = Member.objects.get(id=memberID)
    member.delete()
    messages.success(request, 'Member deleted successfully.')
    return redirect("member")

def issue_book_list(request):
    issued = Transaction.objects.all()
    return render(request, "issue_list.html", {"issued": issued})

def issue_book(request):
    if request.method == "GET":
        books = Book.objects.all()
        members = Member.objects.all()
        return render(request, "issue_book.html", {"books": books, "members": members})

    if request.method == "POST":
        member_email = request.POST.get("member_name")
        book_id = request.POST.get("book_name")
        return_date_str = request.POST.get("return_date")

        return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()

        member = Member.objects.get( email=member_email)
        book = Book.objects.get( bookID=book_id)

        today = datetime.now().date()
        days_borrowed = (return_date - today).days
        rent_fee = days_borrowed * 10 if days_borrowed >= 0 else 0

        if member.debt + rent_fee > 500:
            messages.error(request, "Member's debt exceeds Rs. 500. Book cannot be issued")
            return render(request, "issue_book.html")

        Transaction.objects.create(member=member, book=book, return_date=return_date, rent_fee=rent_fee)

        transactions_for_member = Transaction.objects.filter(member=member)
        total_debt = sum(transaction.rent_fee for transaction in transactions_for_member)
        member.debt = total_debt
        member.save()
        messages.success(request, "Book issued successfully")

        return redirect("issue-book")

def collect_fee(request, transaction_id):
    transaction = Transaction.objects.get( pk=transaction_id)

    if transaction.rent_fee > 0:
        member = transaction.member
        member.debt -= transaction.rent_fee
        member.save()

        transaction.rent_fee = 0
        transaction.save()

    return redirect('issue-list')
