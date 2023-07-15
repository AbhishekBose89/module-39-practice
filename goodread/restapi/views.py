from django.http import JsonResponse, HttpResponseBadRequest
import json
from .models import *
from .serializer import *
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Q, Sum

# Create your views here.


class CreateBook(View):
    def post(self, request):
        data = json.loads(request.body)
        serialized_data = BookSerializer(data=data)
        try:
            if serialized_data.is_valid():
                Book.objects.create(**data)
                return JsonResponse(serialized_data.data, safe=False, status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


class BookView(View):
    def get(self, request):
        books = Book.objects.all()
        serialized_book = BookSerializer(books, many=True).data
        return JsonResponse(serialized_book, safe=False, status=200)


class GetBookById(View):
    def get(self, request, book_id):
        try:
            book_found = Book.objects.get(book_id=book_id)
            if book_found:
                return JsonResponse(
                    BookSerializer(book_found).data, safe=False, status=200
                )
            else:
                return JsonResponse({"msg": "No book found"})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


class SearchBook(View):
    def get(self, request):
        query = request.GET.get("query")
        try:
            books = Book.objects.filter(title=query)
            if books:
                serialized_books = []
                for book in books:
                    serialized_books.append(BookSerializer(book).data)
                return JsonResponse(serialized_books, safe=False, status=200)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


class CreateReview(View):
    def post(self, request):
        data = json.loads(request.body)
        serialized_data = BookReviewSerializer(data=data)
        try:
            if serialized_data.is_valid():
                BookReview.objects.create(**data)
                return JsonResponse(serialized_data.data, safe=False, status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


class GetReviews(View):
    def get(self, request):
        reviews = BookReview.objects.all()
        serialized_reviews = BookReviewSerializer(reviews, many=True).data
        return JsonResponse(serialized_reviews, safe=False, status=200)


class UpdateReview(View):
    def put(self, request, review_id):
        review_data = json.loads(request.body)
        serialized_review_data = BookReviewSerializer(data=review_data)
        try:
            if serialized_review_data.is_valid():
                review = BookReview.objects.get(review_id=review_id)
                for key, value in review_data.items():
                    setattr(review, key, value)
                    review.save()
                return JsonResponse(serialized_review_data.data, safe=False)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


class DeleteReview(View):
    def delete(self, request, review_id):
        try:
            review = BookReview.objects.get(review_id=review_id)
            review.delete()
            return JsonResponse({"msg": "Review is deleted successfully"}, status=200)
        except Exception as e:
            return HttpResponseBadRequest(str(e))


class Signup(View):
    def post(self, request):
        user_data = json.loads(request.body)
        serialized_user_data = UserSerializer(data=user_data)
        try:
            if serialized_user_data.is_valid():
                User.objects.create(**user_data)
                return JsonResponse(
                    {"msg": "User is registered successfully"}, status=201
                )
        except Exception as e:
            HttpResponseBadRequest(str(e))


class Signin(View):
    def post(self, request):
        user_data = json.loads(request.body)
        user_data.pop("name", None)
        serialized_user_data = UserSerializer(data=user_data)
        try:
            if serialized_user_data.is_valid():
                user = User.objects.get(
                    email=user_data["email"], password=user_data["password"]
                )
                if user:
                    return JsonResponse({"msg": "Login Successful"}, status=200)
                else:
                    return JsonResponse({"msg": "Login Failed.Try Again"})
        except Exception as e:
            return HttpResponseBadRequest(str(e))


class GetReviewWithUser(View):
    def get(self, request, review_id):
        review = BookReview.objects.filter(review_id=review_id).first()
        if review:
            user = User.objects.filter(user_id=review.user_id).first()
            response_data = {
                "review_id": review.review_id,
                "book_id": review.book_id,
                "user": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                },
                "comment": review.comment,
                "rating": review.rating,
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"msg": "Review not found"})


# class GetUserReviews(View):
#     def get(self, request, user_id):
#         user = User.objects.filter(user_id=user_id).first()
#         if user:
#             reviews = BookReview.objects.filter(user_id=user_id)
#             review_list = []
#             for review in reviews:
#                 each_review = {
#                     "review_id": review.review_id,
#                     "book_id": review.book_id,
#                     "comment": review.comment,
#                     "rating": review.rating,
#                 }
#                 review_list.append(each_review)
#             response_data = {
#                 "user_id": user.user_id,
#                 "name": user.name,
#                 "email": user.email,
#                 "reviews": review_list,
#             }
#             return JsonResponse(response_data)
#         else:
#             return JsonResponse({"msg": "user not found"})


class GetUserReviews(View):
    def get(self, request, user_id):
        user = User.objects.filter(user_id=user_id).first()
        if user:
            reviews = BookReview.objects.filter(user_id=user_id).values()
            serialized_user = UserSerializer(user).data
            serialized_user["reviews"] = list(reviews)
            return JsonResponse(serialized_user, safe=False)
        else:
            return JsonResponse({"msg": "user not found"})


class GetAuthorsByBook(View):
    def get(self, request, book_id):
        book = Book.objects.filter(book_id=book_id).first()
        if book:
            authors = book.authors.all()
            author_list = []
            for author in authors:
                author_data = {"author_id": author.author_id, "name": author.name}
                author_list.append(author_data)
            response_data = {
                "book_id": book.book_id,
                "title": book.title,
                "authors": author_list,
                "price": book.price,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({"msg": "No such data found."})


class GetBooksByAuthor(View):
    def get(self, request, author_id):
        author = Author.objects.filter(author_id=author_id).first()
        if author:
            books = author.books.all()
            book_list = []
            for book in books:
                book_data = {
                    "book_id": book.book_id,
                    "title": book.title,
                    "price": book.price,
                }
                book_list.append(book_data)
            response_data = {
                "author_id": author_id,
                "name": author.name,
                "books": book_list,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({"msg": "No such data found"})


class SearchBookApi(View):
    def get(self, request, search_text):
        books = Book.objects.filter(title__icontains=search_text)
        if books:
            serialized_book = []
            for book in books:
                book_data = {
                    "book_id": book.book_id,
                    "title": book.title,
                    "price": book.price,
                }
                serialized_book.append(book_data)
            return JsonResponse(serialized_book, safe=False)
        else:
            return JsonResponse({"msg": "Searching books are not present"})


class FilteredBook(View):
    def get(self, request):
        title = request.GET.get("title", "")
        min_price = request.GET.get("min", 0)
        max_price = request.GET.get("max", 0)
        books = Book.objects.all()
        if title:
            books = books.filter(title__icontains=title)
        if min_price:
            books = books.filter(price__gte=min_price)
        if max_price:
            books = books.filter(price__lte=max_price)
        if books:
            # serialized_books=BookSerializer(books,many=True).data
            serialized_books = [
                {"book_id": book.book_id, "title": book.title, "price": book.price}
                for book in books
            ]
            return JsonResponse(serialized_books, safe=False)
        else:
            return JsonResponse({"msg": "Filtered books are not found"})


class PaginatedBooks(View):
    def get(self, request):
        page = request.GET.get("page", 1)
        books = Book.objects.all()
        paginator = Paginator(books, 3)
        page = paginator.get_page(page)
        book_obj = page.object_list
        serialized_books = BookSerializer(book_obj, many=True).data
        return JsonResponse(
            {
                "data": serialized_books,
                "Total_books": books.count(),
                "total_pages": paginator.num_pages,
            }
        )


class GetBookByPriceAuthor(View):
    def get(self, request):
        author = request.GET.get("author")
        price = request.GET.get("price")
        books = Book.objects.filter(
            Q(price__gt=price) & Q(authors__name__icontains=author)
        )
        response = [{"book_name": book.title, "price": book.price} for book in books]
        return JsonResponse(response, safe=False)


class GetTotalPrice(View):
    def get(self, request):
        price_query = request.GET.get("price")
        author=request.GET.get("author")
        books = Book.objects.filter(Q(price__gt=price_query) & Q(authors__name__icontains=author)).aggregate(sum=Sum("price"))
        response = {"sum": books["sum"]}
        return JsonResponse(response)
