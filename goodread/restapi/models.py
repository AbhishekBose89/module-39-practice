from django.db import models

# from pymongo import IndexModel
from django.db.models import Index


# Create your models here.
# class Book(models.Model):
#     book_id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=300)
#     price = models.FloatField()


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name="books")
    price = models.FloatField()

    class Meta:
        indexes = [
            Index(
                fields=["-price", "title"],
                name="price-title-index",
            ),
            Index(fields=["price"], name="price-index"),
        ]


class BookReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    user_id = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    rating = models.FloatField()


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=300)
    password = models.CharField(max_length=16)
