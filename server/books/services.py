from email import message
from .models import Book
from django_grpc_framework import generics
from .serializers import RetrieveBookRequestSerializer, ListBookRequestSerializer, CreateBookProtoSerializer
from django.db.models import Q
from grpc_server.proto.books_pb2 import BookResponse


class BookService(generics.ModelService):
    queryset = Book.objects
    serializer_class = RetrieveBookRequestSerializer
    

    def RetrieveBook(self, request, context):
        serializer = RetrieveBookRequestSerializer(message=request)
        if serializer.is_valid():
            id = serializer.validated_data.get("book_id")
            book = self.queryset.get(id=id)
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
        else:
            return None
    def ListBook(self, request, context):
        serializer = ListBookRequestSerializer(message=request)
        if serializer.is_valid():
            start_year = serializer.validated_data.get("start")
            end_year = serializer.validated_data.get("end")
            if start_year and end_year:
                filter = Q(year__gte=start_year) & Q(year__lte=end_year)

                for book in self.queryset.filter(filter):
                    print(book)
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

            else:
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
            
    def CreateBook(self, request, context):
        serializer = CreateBookProtoSerializer(message=request)
        if serializer.is_valid():
            book = self.queryset.create(
                author=serializer.validated_data.get("author"),
                country=serializer.validated_data.get("country"),
                language=serializer.validated_data.get("language"),
                link=serializer.validated_data.get("link"),
                pages=serializer.validated_data.get("pages"),
                title=serializer.validated_data.get("title"),
                year=serializer.validated_data.get("year"),
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
