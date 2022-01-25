from .models import Book
from django_grpc_framework import generics
from .serializers import BookProtoSerializer
from django.db.models import Q
from grpc_server.proto.books_pb2 import BookResponse


class BookService(generics.ModelService):
    queryset = Book.objects
    serializer_class = BookProtoSerializer

    def ListBook(self, request, context):
        start_year = request.start
        end_year = request.end

        if start_year and end_year:
            filter = Q(year__gte=start_year) & Q(year__lte=end_year)
            for book in self.queryset.filter(filter):
                yield BookResponse(
                    book_id=book.id,
                    author=book.author,
                    country=book.country,
                    language=book.language,
                    link=book.link,
                    pages=book.pages,
                    title=book.title,
                    year=book.year,
                )

        for book in self.queryset.all():
            yield BookResponse(
                book_id=book.id,
                author=book.author,
                country=book.country,
                language=book.language,
                link=book.link,
                pages=book.pages,
                title=book.title,
                year=book.year,
            )

    def RetrieveBook(self, request, context):
        book = self.queryset.get(id=request.book_id)

        return BookResponse(
            book_id=book.id,
            author=book.author,
            country=book.country,
            language=book.language,
            link=book.link,
            pages=book.pages,
            title=book.title,
            year=book.year,
        )

    def CreateBook(self, request, context):
        book = self.queryset.create(
            author=request.author,
            country=request.country,
            language=request.language,
            link=request.link,
            pages=request.pages,
            title=request.title,
            year=request.year,
        )
        return BookResponse(
            book_id=book.id,
            author=book.author,
            country=book.country,
            language=book.language,
            link=book.link,
            pages=book.pages,
            title=book.title,
            year=book.year,
        )
