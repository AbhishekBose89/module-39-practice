from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path("books/create/", csrf_exempt(CreateBook.as_view()), name="create-book"),
    path("books/", BookView.as_view(), name="view-all-books"),
    path("books/<int:book_id>/", GetBookById.as_view(), name="get-book-by-id"),
    path("books/search/", SearchBook.as_view(), name="search-book"),
    path("reviews/create/", csrf_exempt(CreateReview.as_view()), name="create-review"),
    path("reviews/", GetReviews.as_view(), name="get-all-reviews"),
    path(
        "reviews/<int:review_id>/update/",
        csrf_exempt(UpdateReview.as_view()),
        name="update-review",
    ),
    path(
        "reviews/<int:review_id>/delete/",
        csrf_exempt(DeleteReview.as_view()),
        name="delete-review",
    ),
    path("user/signup/", csrf_exempt(Signup.as_view()), name="user-signup"),
    path("user/signin/", csrf_exempt(Signin.as_view()), name="user-signin"),
    path(
        "reviews/<int:review_id>/userDetails/",
        csrf_exempt(GetReviewWithUser.as_view()),
        name="get-review-with-user",
    ),
    path(
        "users/<int:user_id>/reviews/",
        csrf_exempt(GetUserReviews.as_view()),
        name="get-user-reviews",
    ),
    path(
        "books/<int:book_id>/authors/",
        csrf_exempt(GetAuthorsByBook.as_view()),
        name="get-authors-by-book",
    ),
    path(
        "authors/<int:author_id>/books/",
        csrf_exempt(GetBooksByAuthor.as_view()),
        name="get-books-by-author",
    ),
    path(
        "book/search/<str:search_text>",
        csrf_exempt(SearchBookApi.as_view()),
        name="search-book-by-search_text",
    ),
    path("book/", csrf_exempt(FilteredBook.as_view()), name="filtered-book"),
    path("book/page/", csrf_exempt(PaginatedBooks.as_view()), name="paginated-books"),
]
