from django.urls import path
from .views import *

urlpatterns = [
    
    path("", book_list, name="book-list" ),
    path("update-book/<int:book_id>/", update_book, name="update-book"),
    path("add-book/", book_create, name="add-book" ),
    path("delete-book/<int:pk>/", delete_book, name="delete-book" ),
    path("add-member/", create_member, name="add-member" ),
    path("member/", members, name="member" ),
    path('update-member/<int:memberID>/', update_member, name='update-member'),

    path("delete-member/<int:memberID>/", delete_member, name="delete-member" ),
    path("issue-book", issue_book, name="issue-book"),
    path("issue-list", issue_book_list, name="issue-list"),
    path('collect_fee/<int:transaction_id>/', collect_fee, name='collect-fee'),

]
