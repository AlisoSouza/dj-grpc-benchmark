import os
import grpc
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from grpc_server.proto import books_pb2_grpc, books_pb2
from concurrent import futures
from books.models import Book
from django.db.models import Q

class BookService(
    books_pb2_grpc.BookControllerServicer
):
    queryset = Book.objects

    def ListBook(self, request, context):
        if request.start:
            filter = Q(year__gte=request.start) & Q(year__lte=request.end)
            for book in self.queryset.filter(filter):
                yield books_pb2.BookResponse(
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
                yield books_pb2.BookResponse(
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
        return books_pb2.BookResponse(
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
        
        return books_pb2.BookResponse(
            book_id=book.id,
            author=book.author,
            country=book.country,
            language=book.language,
            link=book.link,
            pages=book.pages,
            title=book.title,
            year=book.year,
        )
 


def serve():
    port = "[::]:50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookControllerServicer_to_server(
        BookService(), server
    )
    server.add_insecure_port(port)
    server.start()
    print(f"Running server on port {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()